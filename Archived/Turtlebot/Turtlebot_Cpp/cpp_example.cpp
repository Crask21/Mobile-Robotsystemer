#include <iostream>
#include <chrono>
#include <thread>
#include <csignal> // Catch sigterm (CTRL + C)
#include "mqtt/async_client.h"
#include "json.hpp"

using namespace std;
using json = nlohmann::json;

//const string ADDRESS { "tcp://192.168.0.6:1883" };
const string ADDRESS { "tcp://localhost:1883" };
const string TOPIC { "cmd_vel" };
const int QOS = 1;

// Declared globally as signal handler can't be part of the class..
mqtt::async_client* cli;
mqtt::topic* top;
mqtt::token_ptr tok;

// Handle CTRL + C and stop the robot
void signalHandler(int signum) {
    json stop_msg = {{"linear", {{"x", 0.0}, {"y", 0}, {"z", 0}}},
    {"angular", {{"x", 0}, {"y", 0}, {"z", 0.0}}}
    };
    cout << "CTRL + C pressed, exiting.." << endl;
    tok = top->publish(stop_msg.dump());
    tok->wait();
    exit(signum);
}

/////////////////////////////////////////////////////////////////////////////

class Example {
    public:
        Example(mqtt::async_client& client, mqtt::topic& topic) {
            cli = &client;
            top = &topic;
        }
        ~Example() {}

        bool connect() {
            try {
                cout << "\nConnecting..." << endl;
                cli->connect()->wait();
                cout << "  ...OK" << endl;
            }
            catch (const mqtt::exception& exc) {
                cerr << exc << endl;
                return false;
            }
            return true;
        }

        void publish_message(json j) {
            try {
                tok = top->publish(j.dump());
                tok->wait();
            }
            catch (const mqtt::exception& exc) {
                cerr << exc << endl;
                return;
            }
        }
};

int main(int argc, char* argv[])
{
    signal(SIGINT, signalHandler);
	cout << "Initializing for server '" << ADDRESS << "'..." << endl;
    mqtt::async_client cli(ADDRESS, "");
    mqtt::topic top(cli, TOPIC, QOS);

    Example ex(cli, top);
    bool connected = ex.connect();
    cout << "Connected: " << connected << endl;

    // Modify linear x (forward velocity) and angular z (angular velocity)
    json j = {
        {"linear", {{"x", 0.0}, {"y", 0}, {"z", 0}}},
        {"angular", {{"x", 0}, {"y", 0}, {"z", 0.5}}}
    };
    
    while(true){
        ex.publish_message(j);
        // Sleep 200 ms
        this_thread::sleep_for(chrono::milliseconds(200));
    }
    cout << "Done" << endl;

 	return 0;
}