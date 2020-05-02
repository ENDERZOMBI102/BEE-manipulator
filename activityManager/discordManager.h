#pragma once
#include <iostream>
#include "discordsdk/discord.h"
#include <ctype.h>

class discordManager {
public:
    //declare variables and objects
    discord::Core* core{};
    discord::Activity activity{};
    discord::ActivitySecrets secret{};
    lastUpdate lastData;
    int64_t client_id;
    std::string appName;

    //costructor
    discordManager();
    //decostructor
    ~discordManager();

    void initDiscord(int64_t client_id, std::string appName_par, const char* exe_path);
    void tick();
    void close();
    void updatePresence(presenceStruct presence);
    DiscordActivity presenceToActivity();

};

typedef struct lastUpdate {
    //activity
    std::string state;
    std::string details;
    //activity timestamps
    int64_t startTimestamp = NULL;
    //activity assets
    std::string largeImage;
    std::string largeText;
    std::string smallImage;
    std::string smallText;
    //activity secrets
    std::string spectateSecret;
};
typedef struct presenceStruct {
    //activity
    std::string state;
    std::string details;
    //activity timestamps
    int64_t startTimestamp = NULL;
    //activity assets
    std::string largeImage;
    std::string largeText;
    std::string smallImage;
    std::string smallText;
    //activity secrets
    std::string spectateSecret;
};

typedef struct userStruct {
    int64_t id;
    std::string username;
    std::string discriminator;
    std::string avatar;
};