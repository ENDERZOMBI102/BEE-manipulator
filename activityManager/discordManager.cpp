#include "discordManager.hpp"
#define DLL_EXPORT_API __declspec(dllexport)

discordManager::discordManager() {
    this->lastUpdateSucceded = true;
    this->lastData;
}
discordManager::~discordManager() {}


void discordManager::initDiscord(int64_t client_id_par = NULL, std::string appName_par = NULL, const char* exe_path = NULL) {
    if (client_id_par != NULL ) {
        throw new std::exception("no client_id given!");
    }
    client_id = client_id_par;
    appName = appName_par;
    do {//client id     flag (1 fa si che non si richieda discord aperto)   instance (istanza da inizializzare)
        discord::Core::Create(client_id, 1, &core);// init the discord core
    } while (!core);
    //core->ActivityManager().RegisterCommand( exe_path );
}

void discordManager::tick() {
    core->RunCallbacks();
    core->ActivityManager().OnActivitySpectate.Connect([](const char* secret) { std::cout << "Spectate " << secret << "\n"; });
}

void discordManager::close() {
    delete[] core;
}

bool discordManager::updatePresence(presenceStruct& presence) {
    /*
    * if any of those are in the struct, apply them to the lastData, so we don't have to rewrite everything
    * twice twice in the parameter
    */
    //save last data struct
    presenceStruct lastData = this->lastData;
    presenceStruct tmpData = lastData;
    if (!presence.state.empty()) { lastData.state = presence.state; }
    if (!presence.details.empty()) { lastData.details = presence.details; }
    if (!presence.startTimestamp == NULL) { lastData.startTimestamp = presence.startTimestamp; }
    if (!presence.largeImage.empty()) { lastData.largeImage = presence.largeImage; }
    if (!presence.largeText.empty()) { lastData.largeText = presence.largeText; }
    if (!presence.smallImage.empty()) { lastData.smallImage = presence.smallImage; }
    if (!presence.smallText.empty()) { lastData.smallText = presence.smallText; }
    if (!presence.spectateSecret.empty()) { lastData.spectateSecret = presence.spectateSecret; }
    //if something changed, update the activity with new data
    if (!(tmpData == lastData) || !lastUpdateSucceded) {// the or so we don't skip any data
        //the function names says everything you need to know
        activity.SetDetails(lastData.details.c_str());
        activity.SetState(lastData.state.c_str());
        activity.GetTimestamps().SetStart(discord::Timestamp(lastData.startTimestamp));//get can use set (what)
        activity.GetAssets().SetSmallImage(lastData.smallImage.c_str());
        activity.GetAssets().SetSmallText(lastData.smallText.c_str());
        activity.GetAssets().SetLargeImage(lastData.largeImage.c_str());
        activity.GetAssets().SetLargeText(lastData.largeText.c_str());
        activity.GetSecrets().SetSpectate(lastData.spectateSecret.c_str());
        activity.SetType(discord::ActivityType::Playing);
    }
    //and FINALLY update the activity (aka RPC) with callback
    core->ActivityManager().UpdateActivity(activity, this->activityCallback);
    return lastUpdateSucceded;
}

void discordManager::activityCallback(discord::Result result) {
    //this make you know if the last update succeded
    this->lastUpdateSucceded = result == discord::Result::Ok ? true : false;
}