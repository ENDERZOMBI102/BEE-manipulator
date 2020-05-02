#include "discordManager.h"
#define DLL_EXPORT_API __declspec(dllexport)

discordManager::discordManager() {}
discordManager::~discordManager() {}


void discordManager::initDiscord(int64_t client_id_par = NULL, std::string appName_par = NULL, const char* exe_path) {
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

void discordManager::updatePresence(presenceStruct presence) {
    /*
    * if any of those are in the struct, apply them to the lastData, so we don't have to rewrite everything
    * twice twice in the parameter
    */
    if (!presence.state.empty()) { lastData.state == presence.state; }
    if (!presence.details.empty()) { lastData.details == presence.details; }
    if (!presence.startTimestamp == NULL) { lastData.startTimestamp == presence.startTimestamp; }
    if (!presence.largeImage.empty()) { lastData.largeImage == presence.largeImage; }
    if (!presence.largeText.empty()) { lastData.largeText == presence.largeText; }
    if (!presence.smallImage.empty()) { lastData.smallImage == presence.smallImage; }
    if (!presence.smallText.empty()) { lastData.smallText == presence.smallText; }
    if (!presence.spectateSecret.empty()) { lastData.spectateSecret == presence.spectateSecret; }
    
    DiscordActivity activity = presenceToActivity();
}

DiscordActivity discordManager::presenceToActivity() {
    /*
    * this function convert from a custom
    *
    */


    // discord activity assets, part of discord activity struct
    DiscordActivityAssets assets;
    strcpy(assets.large_image, lastData.largeImage.c_str());
    strcpy(assets.large_text, lastData.largeText.c_str());
    strcpy(assets.small_image, lastData.smallImage.c_str());
    strcpy(assets.small_text, lastData.smallText.c_str());
    // discord activity timestamps, part of discord activity
    DiscordActivityTimestamps timestamps;
    timestamps.start = lastData.startTimestamp;
    // discord activity secrets, part of discord activity
    DiscordActivitySecrets secrets;
    strcpy(secrets.spectate, lastData.spectateSecret.c_str());
    // main part of the discord activity
    DiscordActivity activity;
    activity.application_id = client_id;
    strcpy(activity.name, appName.c_str());
    strcpy(activity.state, lastData.state.c_str());
    strcpy(activity.details, lastData.details.c_str());
    activity.timestamps = timestamps;
    activity.assets = assets;
    activity.secrets = secrets;
    return activity;
}