package de.fhkiel.aem;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Input;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.Sprite;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.math.Circle;
import com.badlogic.gdx.utils.TimeUtils;

import java.util.HashMap;

/**
 * The Bird of the Game.
 */
public class Bird {
    private final Sprite birdSprite;
    private final Circle hitbox;
    private final Texture mannyStraight = new Texture(Gdx.files.internal(Configuration.manny_straightImg));
    private final Texture mannyUp = new Texture(Gdx.files.internal(Configuration.manny_upImg));
    private final Texture mannyDown = new Texture(Gdx.files.internal(Configuration.manny_downImg));
    private final Texture mannyStraightHelm = new Texture(Configuration.manny_straight_helmImg);
    private final Texture mannyDownHelm = new Texture(Configuration.manny_down_HelmImg);
    private final Texture mannyUpHelm = new Texture(Configuration.manny_up_helmImg);
    private final Texture mannyUpSpace = new Texture(Configuration.mannyUpSpace);
    private final Texture mannyUpSpaceHelmet = new Texture(Configuration.mannyUpSpaceHelmet);
    private final Texture mannyDownSpace = new Texture(Configuration.mannyDownSpace);
    private final Texture mannyDownSpaceHelmet = new Texture(Configuration.mannyDownSpaceHelmet);
    private final Texture mannyStraightSpace = new Texture(Configuration.mannyStraightSpace);
    private final Texture mannyStraightSpaceHelmet = new Texture(Configuration.mannyStraightSpaceHelmet);


    private final int width = 100;
    private float highscore = 0;
    private int scoreCollectable = 0;
    private boolean invincible = false;
    private boolean helmetactive = false;
    private int multiplier = 1;
    public int birdRotation = 0;
    private boolean birdMayRotate = false;
    private int birdWidth = 350;
    private long lastMultiplierTime;
    private long lastShrinkTime;
    public boolean spaceScreen = false;
    private long dieTime = 0;
    private static HashMap<Integer, Texture> animationMap = new HashMap<>();
    private Texture mannyStare;
    private boolean spaceManni = false;


    public Texture getMannyStraight() {
        if(spaceManni){
            return mannyStraightSpace;
        }else {
            return mannyStraight;
        }
    }

    public Texture getMannyStraightSpace() {return mannyStraightSpace;}

    //bestimmt die Beschleunigung, in der der Vogel nach unten fällt
    private float fallSpeed = 200;
    private long pressTime;

    /**
     * Creates an new bird object on the given location.
     *
     * @param xPos x position of the bird
     * @param yPos y position of the bird
     */
    public Bird(float xPos, float yPos, boolean spaceManniActive) {
        spaceManni = spaceManniActive;
        if(spaceManni) {
            mannyStare = new Texture(Gdx.files.internal(Configuration.manniSpaceBtn + "-hover.png"));
        }
        else {
            mannyStare = new Texture(Gdx.files.internal(Configuration.manny_heyImg));
        }
        birdSprite = new Sprite(mannyStare);

        birdSprite.setX(xPos);
        birdSprite.setY(yPos);

        hitbox = new Circle(birdSprite.getX(), birdSprite.getY(), width / 2f);
        hitbox.setPosition(birdSprite.getX() + hitbox.radius, birdSprite.getY() + hitbox.radius);
        initializeAnimation();
    }

    /**
     * Renders the bird on the given SpriteBatch.
     *
     * @param batch spriteBatch it rendered on
     */
    public void render(SpriteBatch batch) {
        batch.draw(birdSprite, birdSprite.getX(), birdSprite.getY(), birdSprite.getX()-25, birdSprite.getX()-25,
                getBirdWidth(), getBirdWidth(), 1, 1, birdRotation);
    }

    /**
     * Moves the Bird.
     */
    public void move(float deltaTime) {
        birdGetSmaller();

        //bird rotiert nach oben bis er seine Grenze erreicht und dann wieder zurück
        if (birdMayRotate && birdRotation < 25) {
            birdRotation += 4;
        } else if (birdRotation > 0) {
            birdRotation -= 2d;
        }

        //bird Fällt nach unten mit einer Beschleunigung
        birdSprite.setY(birdSprite.getY() - fallSpeed * deltaTime);
        hitbox.setY(hitbox.y - fallSpeed * deltaTime);
        fallSpeed += 20;

        if (Gdx.input.isKeyJustPressed(Input.Keys.SPACE) || Gdx.input.justTouched()) {
            sprungNachOben();
        }

        //nach xxxx millisec nachdem der button betätigt wurde, fällt der Vogel auf 2 Phasen wieder runter
        if (pressTime != 0 && (fallSpeed < 0 && TimeUtils.millis() >= (pressTime + 200))) {

            if(spaceScreen || spaceManni) {
                if (helmetactive) {
                    birdSprite.setTexture(mannyStraightSpaceHelmet);
                } else {
                    birdSprite.setTexture(mannyStraightSpace);
                }
            }
            else {
                if (helmetactive) {
                    birdSprite.setTexture(mannyStraightHelm);
                } else {
                    birdSprite.setTexture(mannyStraight);
                }
            }
            fallSpeed = 320;
            birdMayRotate = false;
        }
        if (pressTime != 0 && fallSpeed > 0 && TimeUtils.millis() >= (pressTime + 300)) {
            if(spaceScreen || spaceManni) {
                if (helmetactive) {
                    birdSprite.setTexture(mannyStraightSpaceHelmet);
                } else {
                    birdSprite.setTexture(mannyStraightSpace);
                }
            }
            else {
                if (helmetactive) {
                    birdSprite.setTexture(mannyStraightHelm);
                } else {
                    birdSprite.setTexture(mannyStraight);
                }
            }
            fallSpeed = 440;
            pressTime = 0;
        }
        //stoppe den Vogel am Rand des Bilds
        if (birdSprite.getY() <= 50) {
            slide();
        }

    }

    //zum beginn des playScreens wird der Vogel allmählich klein
    public void birdGetSmaller() {
        if (birdWidth > 100) {
            this.setBirdWidth(this.getBirdWidth() - 5);
        }
    }

    /**
     * Gets the Sprite of the bird.
     *
     * @return The bird Sprite
     */
    public Sprite getBirdSprite() {
        return birdSprite;
    }

    /**
     * Returns the hitbox of the bird.
     *
     * @return Circle that represents the hitbox
     */
    public Circle getHitbox() {
        return hitbox;
    }

    /**
     * Gets the width of the Bird.
     *
     * @return Width of bird
     */
    public int getWidth() {
        return width;
    }


    public int getBirdWidth() {
        return birdWidth;
    }

    public void setBirdWidth(int birdWidth) {
        this.birdWidth = birdWidth;
    }

    /**
     * Gets the highscore.
     *
     * @return The highscore
     */
    public float getHighscore() {
        return highscore;
    }

    /**
     * Sets the highscore to a new value.
     *
     * @param highscore New highscore
     */
    public void setHighscore(float highscore) {
        this.highscore = highscore;
    }

    /**
     * The bird jumps up.
     */
    private void sprungNachOben() {
        if (birdRotation < 25) {
            birdMayRotate = true;
        }
        pressTime = TimeUtils.millis();
        if(spaceScreen || spaceManni) {
            if (helmetactive) {
                birdSprite.setTexture(mannyUpSpaceHelmet);
            } else {
                birdSprite.setTexture(mannyUpSpace);
            }
        }
        else {
            if (helmetactive) {
                birdSprite.setTexture(mannyUpHelm);
            } else {
                birdSprite.setTexture(mannyUp);
            }
        }
        fallSpeed = -850;
    }

    private void slide() {
        pressTime = TimeUtils.millis();
        if(spaceScreen || spaceManni) {
            if (helmetactive) {
                birdSprite.setTexture(mannyDownSpaceHelmet);
            } else {
                birdSprite.setTexture(mannyDownSpace);
            }
        }
        else {
            if (helmetactive) {
                birdSprite.setTexture(mannyDownHelm);
            } else {
                birdSprite.setTexture(mannyDown);
            }
        }
        fallSpeed = -400;
    }

    /**
     * the Bird dies and the Animation changes
     * eine Reihe an Bildern wird abgespielt
     * und der Vogel dreht sich um seine x Achse beim Fallen
     */
    public void birdDies() {
        fallSpeed = 1;
        birdSprite.setY(birdSprite.getY() - fallSpeed);

        int dieStep = dieStep();
        if (dieStep < 8) {
            birdSprite.setTexture(animationMap.get(dieStep));
        } else {
            fallSpeed = 4;
            birdSprite.setY(birdSprite.getY() - fallSpeed);
        }
        birdMayRotate = true;
        birdRotation += 8;
    }

    /**
     * return an integer based on the time of the collision
     * the return number presents the dying step
     */
    private int dieStep() {
        return (int) ((TimeUtils.millis() - dieTime) / 100);
    }

    public void setFallSpeed(float fallSpeed) {
        this.fallSpeed = fallSpeed;
    }

    public int getScoreCollectable() {
        return scoreCollectable;
    }

    public void setScoreCollectable(int scoreCollectable) {
        this.scoreCollectable = scoreCollectable;
    }

    /*public Texture getMannyUp() {
        return mannyUp;
    }

    public Texture getMannyDown() {
        return mannyDown;
    }*/

    public boolean isInvincible() {
        return invincible;
    }

    public Texture getMannyStraightSpaceHelmet() {
        return mannyStraightSpaceHelmet;
    }

    public void setInvincible(boolean invincible) {
        this.invincible = invincible;
    }

    /*public float getFallSpeed() {
        return fallSpeed;
    }

    public long getPressTime() {
        return pressTime;
    }

    public void setPressTime(long pressTime) {
        this.pressTime = pressTime;
    }*/

    public Texture getMannyStraightHelm() {
        return mannyStraightHelm;
    }

    /*public Texture getMannyDownHelm() {
        return mannyDownHelm;
    }

    public Texture getMannyUpHelm() {
        return mannyUpHelm;
    }*/

    public boolean isHelmetactive() {
        return helmetactive;
    }

    public void setHelmetactive(boolean helmetactive) {
        this.helmetactive = helmetactive;
    }

    public int getMultiplier() {
        return multiplier;
    }

    public void setMultiplier(int multiplier) {
        this.multiplier = multiplier;
    }

    public long getLastMultiplierTime() {
        return lastMultiplierTime;
    }

    public void setLastMultiplierTime(long lastMultiplierTime) {
        this.lastMultiplierTime = lastMultiplierTime;
    }

    public long getLastShrinkTime() {
        return lastShrinkTime;
    }

    public void setLastShrinkTime(long lastShrinkTime) {
        this.lastShrinkTime = lastShrinkTime;
    }

    /*public long getDieTime() {
        return dieTime;
    }*/

    public void setDieTime(long dieTime) {
        this.dieTime = dieTime;
    }

    /**
     * fill the Hashmap with the animation assetss
     */
    private void initializeAnimation() {

        if(spaceScreen || spaceManni){
            animationMap.put(0, new Texture(Gdx.files.internal(Configuration.mannyOuch2Space)));
            animationMap.put(1, new Texture(Gdx.files.internal(Configuration.mannyOuch3Space)));
        }
        else {
            animationMap.put(0, new Texture(Gdx.files.internal(Configuration.mannyOuch2)));
            animationMap.put(1, new Texture(Gdx.files.internal(Configuration.mannyOuch3)));
        }
        animationMap.put(2, new Texture(Gdx.files.internal(Configuration.mannyOuch4)));
        animationMap.put(3, new Texture(Gdx.files.internal(Configuration.mannyOuch5)));
        animationMap.put(4, new Texture(Gdx.files.internal(Configuration.mannyOuch6)));
        animationMap.put(5, new Texture(Gdx.files.internal(Configuration.mannyOuch7)));
        animationMap.put(6, new Texture(Gdx.files.internal(Configuration.mannyOuch8)));
        animationMap.put(7, new Texture(Gdx.files.internal(Configuration.mannyOuch9)));
    }

}
