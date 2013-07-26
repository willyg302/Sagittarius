/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
class SagittariusGame extends UTGame;

var Sagittarius Sag;
var string SagittariusHost;
var int SagittariusPort;

event PreBeginPlay()
{
	super.PreBeginPlay();
	Sag = Spawn(class'Sagittarius');
	Sag.Initialize(SagittariusHost, SagittariusPort);
	// Here you would register any startup modules you might have
}

DefaultProperties
{
	bDelayedStart=false
	SagittariusHost="[APP ID HERE].appspot.com"
	SagittariusPort=80
}