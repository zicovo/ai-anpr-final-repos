# ANPR GSM gebruik achter het stuur

In deze repos staan 6 folders waarvan de inhoud hieronder beschreven staat.

## Aws-rekognition

In deze folder zit een testproject dat in staat is om afeeldingen uit een AWS S3 bucket door de AWS Rekognition api te laten gaan. Deze geeft bijgevolg terug waar een persoon/driver zich bevindt op de foto. 

En aan de hand van die coördinaten, wordt de persoon uit de foto geknipt.

## Driver Cropper Training

Deze folder bevat het model dat gebruikt is om de driver in een auto te herkennen. Er werdt gebruik gemaakt van de Tensorflow 2 API.

## Phone Use Detection Training

Deze folder bevat het model dat gebruikt is om gsm gebruik achter het stuur te detecteren. 

De trainingsdata werd opgedeeld in 5 categorieën.

-Gsm linker oor

-Gsm recher oor

-Linker hand aan het stuur

-Rechter hand aan het stuur

-2 Handen aan het stuur

## image-augmentation-master

Deze folder bevat de code waarmee we onze data geaugment hebben. Elke foto heeft 6 varianten: normal -, low - en high exposure en de geflipte varianten over de y-as.


## Final-project

Final-project bevat een ftp server gemaakt in python die bij het ontvangen van een afbeelding deze door het eerste model laat gaan, het Driver-detection model.

Bijgevolg zal deze afbeelding gecropped worden en door het 2de model gaan, het phone-use-detection model.

De output hiervan zal via een socket server verstuurd worden naar de browser.

RUNNEN: Open een terminal en start het main.py scrypt, dit start de ftp server op.

```bash
python main.py
```

Open een 2de terminal om de socket server op te starten door socker_server.py te runnen.

```bash
python socket_server.py
```

Output van de socket server kan bijgevolg ontvangen worden in de browser door de index.html te openen. 

In de folder zit ook een FTP Settings.png bestand, dit is een screenshot van de storage settings van de camera. Deze kunnen grotendeels letterlijk overgenomen, enkel het ip adres moet je wijzigen naar het gene dat de host van de ftp server op dat moment heeft.

Dit kom je te weten door op windows:

```bash
ipconfig
```

Op linux: 

```bash
ifconfig
```






## License
[MIT](https://choosealicense.com/licenses/mit/)