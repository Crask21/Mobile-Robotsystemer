#include "inc/json.hpp"
#include <iostream>
#include <chrono>
#include <thread>
#include <csignal>
#include "mqtt/async_client.h"

using namespace std;
using json = nlohmann::json;

// Declared globally as signal handler can't be part of the class..
mqtt::async_client* cli;
mqtt::topic* top;
mqtt::token_ptr tok;

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

MoveObj::MoveObj(float speed_ = 0)
{
    setSpeed(speed_)
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