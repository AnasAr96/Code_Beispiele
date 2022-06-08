<h1>Das Programm mus in die richtige Reihnfolge gestartet weren</h1>

<p>1- Als erstes müssen die rohe Daten in dem Ordner Dataset gespeichrt werden, Es spielt keine Rolle wie viele und wie die Datein heißen, wichtig ist dass der inhalt der daten, dem standard der Mockaroo Bennenung  entsprechen</p>

<p>2- Der python Skript make_trainData.py muss einmal laufen. Dieser generiert den Ordner trainData, der mit den trainingsdaten befüllt wird</p>

<p>Die Datei AWS_Train_multimodel.ipynb muss einmal duchlaufen</p>
<h3>Achtung: Die hardgecodeten s3 pfade müssen entsprechend modifiziert werden</h3>
<ul>
    <li>s3_output_path: Der s3 Ordner in den die Artifakte der Modelle gespeichert werden</li>
    <li>code_location: Hier wird die .tar.gz-Datei des Quellverzeichnisses gespeichert</li>
    <li>model_data_prefix: Hier werden die Artifakte der Modelle umbenannt und kopiert, damit sie auf dem Endpoint gehostet werden 
    </li>
</ul>

<p>-3 der Endpoint Name von muli-model muss notiert werden, und das Modell von der Lambda invoken zu konnen.<br>Das findet man in der Sagemaker Konsole unter Inference/Endpoints</p>

<p>-4 Um alles zu löschen und Kosten zu vermeiden, gehen Sie in die Sagemaker Konsole unter Inference/Endpoints und löschen Sie den Endpoint endgültig. Damit der Skript wieder benutzt werden kann, mass man ebenfalls das Modell und die Modellkofiguration in der Sagemaker Konsole löschen</p>
<p></p>


