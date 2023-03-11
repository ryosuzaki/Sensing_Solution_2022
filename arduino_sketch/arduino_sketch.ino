
#include "SPI.h"
#include "Adafruit_GFX.h"
#include "Adafruit_ILI9341.h"
#include <SDHCI.h>
#include <File.h>
#include <Camera.h>

#define TFT_DC 9
#define TFT_CS -1
#define TFT_RST 8

SDClass SD;
Adafruit_ILI9341 tft = Adafruit_ILI9341(&SPI, TFT_DC, TFT_CS, TFT_RST);
int counter=1;
byte data=0;
int posx=0;
int posy=0;
char color="";

void CamCB(CamImage img){
  if(img.isAvailable()){
    img.convertPixFormat(CAM_IMAGE_PIX_FMT_RGB565);
    tft.drawRGBBitmap(0,0,(uint16_t *)img.getImgBuff(),320,240);
    }
}

//void display_predict(int x,int y,String color){
void display_predict(int x,int y){
  tft.fillCircle(x,y, 10,ILI9341_RED);
  //tft.setTextColor(ILI9341_RED);
  //tft.setCursor(1,60);
  //tft.print(color);
}


void setup() {
  Serial.begin(115200);
  tft.begin(40000000);
  tft.setRotation(1);
  
  theCamera.begin();
  theCamera.setStillPictureImageFormat(CAM_IMGSIZE_QVGA_H,CAM_IMGSIZE_QVGA_V,CAM_IMAGE_PIX_FMT_JPG);
  theCamera.startStreaming(true,CamCB);
  
  while (!SD.begin());
  //Serial.println("SD card is mounted.");

  if (SD.beginUsbMsc()) {
    Serial.println("UsbMsc connect error");
  }
}

void loop() {
  /*
  CamImage img=theCamera.takePicture();
  if(img.isAvailable()){
    Serial.println("ccc");
    char path[32]={0};
    sprintf(path,"input_images/img%d.jpg",counter);
    File myFile=SD.open(path,FILE_WRITE | O_TRUNC);
    myFile.write(img.getImgBuff(),img.getImgSize());
    myFile.close();

    Serial.println("A");
    Serial.println(path);
    
    counter=(counter+1)%16;

    while(!Serial.available());
    String phase=Serial.readStringUntil('\n');
    if(phase == "B"){
      //display_predict(Serial.readStringUntil('\n').toInt(),Serial.readStringUntil('\n').toInt(),Serial.readStringUntil('\n'));
      display_predict(Serial.readStringUntil('\n').toInt(),Serial.readStringUntil('\n').toInt());
    }
  }
  Serial.println("bbb");
  */
  CamImage img=theCamera.takePicture();
  if(img.isAvailable()){
    char filename[16]={0};
    sprintf(filename,"input_images/%d.jpg",counter);
    File myFile=SD.open(filename,FILE_WRITE | O_TRUNC);
    //File myFile=SD.open("input_image.jpg",FILE_WRITE | O_TRUNC);
    myFile.write(img.getImgBuff(),img.getImgSize());
    myFile.close();
  }
  if (SD.beginUsbMsc()) {
    Serial.println("UsbMsc connect error");
  }
  Serial.println(counter);
  
  while(!Serial.available());
  if(Serial.read() == 1){
    posx_high=Serial.read();
    posx_low=Serial.read();
    recv_data = makeWord(high,low);
    posy=Serial.read();
    tft.fillCircle(posx, posy, 10,ILI9341_RED);
    tft.setTextColor(ILI9341_RED);
    tft.setCursor(1,60);
    tft.print("Hellow World");
  }
  counter=counter+1;
  if (SD.endUsbMsc()) {
    Serial.println("UsbMsc connect error");
  }
  
}
void readint(){
  
  }
