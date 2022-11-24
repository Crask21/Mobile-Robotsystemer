/* A code class that should handle all audio
for the turtlebot.
*/

#include <iostream>
#include <math.h>
#include <cassert> // only used for error dection and handling
#include <cstddef>
#include "portaudiocpp/PortAudioCpp.hxx"
#include "Sine.h"


const int SAMPLE_RATE;

using namespace std;

class Audio
{
private:
    /* data */
public:
    Audio(int sampleRate, int TableSize = 200): SAMPLE_RATE(sampleRate);
    ~Audio();
};

Audio::Audio(int sampleRate, int TableSize = 200): SAMPLE_RATE(sampleRate)
{
    SineGenerator SineGenerator(TableSize)
}

Audio::~Audio()
{
}
