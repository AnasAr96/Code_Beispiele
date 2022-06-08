package de.fhkiel.aem;

import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.Sprite;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.math.Circle;
import com.badlogic.gdx.math.Rectangle;

/**
 * The barriers the bird can collide with.
 */
public class Barrier {


    private final Sprite barrierSprite;
    public static float speed = 300;
    private float gap = 450;
    private float distance = 850;
    private float wealth;
    private Rectangle hitbox, hitbox2;
    private Circle hitbox3;
    private int hitboxKorrektur = 10;
    private boolean down = false;

    /**
     * Creates a new Barrier on the given location.
     * @param x X position
     * @param y Y position
     * @param imagePath The image of the barrier
     */
    public Barrier(float x, float y, String imagePath, int difficulty){
        barrierSprite = new Sprite(new Texture(imagePath));
        barrierSprite.setX(x);
        barrierSprite.setY(y);

        distance -= difficulty * 100;
        gap -= difficulty * 50;
        wealth = difficulty / 2.0f;

        hitbox = new Rectangle(barrierSprite.getX() + hitboxKorrektur, barrierSprite.getY(),
                barrierSprite.getWidth() - hitboxKorrektur, barrierSprite.getHeight() - 55);
        hitbox2 = new Rectangle(0,0, 60, 40);
        hitbox3 = new Circle(0,0, 6);

    }


    /**
     * Renders the Barrier on the given SpriteBatch.
     * @param batch The SpriteBatch its rendered on
     */
    public void render(SpriteBatch batch){
        batch.draw(barrierSprite, barrierSprite.getX(), barrierSprite.getY(), barrierSprite.getOriginX(), barrierSprite.getOriginY(),
                barrierSprite.getWidth(), barrierSprite.getHeight(),1,1, barrierSprite.getRotation());
    }

    /**
     * Moves the barriers.
     */
    public void move(float deltaTime){
        barrierSprite.setX(barrierSprite.getX() - deltaTime * speed);
        hitbox.setX(hitbox.getX() - deltaTime * speed);
        hitbox2.setX(hitbox2.getX() - deltaTime * speed);
        hitbox3.setX(hitbox3.x - deltaTime * speed);
    }

    /**
     * Gets the Sprite of the barrier.
     * @return The Sprite
     */
    public Sprite getBarrierSprite() {
        return barrierSprite;
    }

    /**
     * Gets the distance between barriers (X distance).
     * @return The Distance
     */
    public float getDistance() {
        return distance;
    }

    /**
     * Gets the hitbox of the barrier.
     * @return The Rectangle hitbox
     */
    public Rectangle getHitbox() {
        return hitbox;}

    /**
     * Gets the gap between the barriers (Y distance).
     * @return The gap
     */
    public float getGap() {
        return gap;
    }

    /**
     * Gets the wealth of the barrier.
     * @return The wealth
     */
    public float getWealth() {
        return wealth;
    }

    /**
     * Sets the wealth of the barrier.
     * @param wealth New wealth
     */
    public void setWealth(float wealth) {
        this.wealth = wealth;
    }

    public Circle getHitbox3() {
        return hitbox3;
    }

    public Rectangle getHitbox2() {
        return hitbox2;
    }

    public boolean isDown() {
        return down;
    }

    public void setDown(boolean down) {
        this.down = down;
    }
}
