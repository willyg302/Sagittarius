/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright WillyG Productions
 * @Authors: William Gaul
 */
class SagittariusGame extends UTGame;

var Sagittarius Sag;
var string SagittariusAppID, SagittariusPass;

event PreBeginPlay()
{
	super.PreBeginPlay();
	Sag = Spawn(class'Sagittarius');
	Sag.Initialize(SagittariusAppID, SagittariusPass);
	// Here you would register any startup modules you might have
}

DefaultProperties
{
	bDelayedStart=false
	SagittariusAppID="[APP ID HERE]"
	SagittariusPass="[APP PASSWORD HERE]"
}