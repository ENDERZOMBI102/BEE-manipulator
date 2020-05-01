#include <iostream>
#include "discordsdk/discord.h"
#include <ctype.h>

#define DLL_EXPORT_API __declspec(dllexport)

DLL_EXPORT_API class discordManager {
public:
    //declare variables and objects
    discord::Core* core{};
    discord::Activity activity{};
    discord::ActivitySecrets secret{};
    //costructor
    discordManager();
    //decostructor
    ~discordManager();
    
    void initDiscord(const char* client_id, const char* exe_path);
    void update();
    void close();
    
};

discordManager::discordManager() {}
discordManager::~discordManager() {}


void discordManager::initDiscord(const char* client_it, const char* exe_path) {
    if (client_it == "" ) {
        throw new std::exception("no client_id given!");
    }
    do {
        discord::Core::Create(461618159171141643, DiscordCreateFlags_Default, &core);// init the discord core
    } while (!core);
    //core->ActivityManager().RegisterCommand( exe_path );
}

void discordManager::update() {
    core->RunCallbacks();
    core->ActivityManager().OnActivitySpectate.Connect([](const char* secret) { std::cout << "Spectate " << secret << "\n"; });
}

void discordManager::close() {
    core->~Core();
    delete this;
}
