#include "sample.h"


char* SampleLine::serialize()
{
    char* buffer = (char*)malloc(sizeof(char)*(data.size()*sizeof(std::complex<float>)));
    for (int i = 0; i < data.size(); i++){
        memcpy(buffer+i*sizeof(std::complex<float>), &data[i], sizeof(std::complex<float>));
    }
    return buffer;
}

void SampleLine::sendToSocket(int socketFd)
{
    char* serialized = serialize();
    helpers::writeNBytes(socketFd, serialized, sizeof(std::complex<float>)*data.size());
    free(serialized);
}

void SampleLine::process()
{
    //TODO: Process each sample line multiplying by a complex phase
    return;
}