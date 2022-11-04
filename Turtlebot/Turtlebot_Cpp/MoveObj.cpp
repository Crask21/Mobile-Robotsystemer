#include "inc/json.hpp"
#include <iostream>
#include <chrono>
#include <thread>
#include <csignal>
#include "mqtt/async_client.h"

//const string ADDRESS { "tcp://192.168.0.6:1883" };
const string ADDRESS { "tcp://localhost:1883" };
const string TOPIC { "cmd_vel" };
const int QOS = 1;

using namespace std;
using json = nlohmann::json;

// Declared globally as signal handler can't be part of the class..
mqtt::async_client* cli;
mqtt::topic* top;
mqtt::token_ptr tok;

void signalHandler(int signum) {
    json stop_msg = {{"linear", {{"x", 0.0}, {"y", 0}, {"z", 0}}},
    {"angular", {{"x", 0}, {"y", 0}, {"z", 0.0}}}
    };
    cout << "CTRL + C pressed, exiting.." << endl;
    tok = top->publish(stop_msg.dump());
    tok->wait();
    exit(signum);
}

class MoveObj
{
private:
    float speed;
    void public message(json j);
public:
    MoveObj(float speed = 0);
    ~MoveObj();
    void setSpeed(float speed_)
    bool straightMove(int distance);
    bool turn(int angle);
    bool curveMove(int radius, int distance);
};

MoveObj::MoveObj(float speed_ = 0, mqtt::async_client& client, mqtt::topic& topic)
{
    setSpeed(speed_)
    cli = &client;
    top = &topic;
}

void MoveObj::setSpeed(float speed_) {
    if (speed_>1)
        speed = 1;
    else if(speed_<-1)
        speed = -1;
    else
        speed = speed_;
}
bool MoveObj::straightMove(int distance) {
    json j = {
        {"linear", {{"x", speed}, {"y", 0}, {"z", 0}}},
        {"angular", {{"x", 0}, {"y", 0}, {"z", 0.5}}}
    };
    float traveltime = distance/speed;
    tok = top->publish(j.dump());
    tok->wait();
}
void MoveObj::publish_message(json j) {
    try {
        tok = top->publish(j.dump());
        tok->wait();
    }
    catch (const mqtt::exception& exc) {
        cerr << exc << endl;
        return;
    }
}