/********************
GNU Radio C++ Flow Graph Source File

Title: Not titled yet
Author: fran
GNU Radio version: v3.8.5.0-6-g57bd109d
********************/

#include "udp_to_filesink.hpp"
using namespace gr;


udp_to_filesink::udp_to_filesink () {



    this->tb = gr::make_top_block("Not titled yet");


// Blocks:
    {
        this->blocks_udp_source_0_0_0 = blocks::udp_source::make(sizeof(int)*16, "192.168.0.21", 12345, 64088, true);
    }
    {
        this->blocks_file_sink_0 = blocks::file_sink::make(sizeof(int)*16, "/run/media/fran/46FAA90DFAA8FA77/Ventanas/IB/PI/GitHub/GNU-Radio/UDP_sock_test/UDP_to_file_sink/file", false);
    }

// Connections:
    this->tb->hier_block2::connect(this->blocks_udp_source_0_0_0, 0, this->blocks_file_sink_0, 0);
}

udp_to_filesink::~udp_to_filesink () {
}

// Callbacks:
int udp_to_filesink::get_samp_rate () const {
    return this->samp_rate;
}

void udp_to_filesink::set_samp_rate (int samp_rate) {
    this->samp_rate = samp_rate;
}


int main (int argc, char **argv) {

    udp_to_filesink* top_block = new udp_to_filesink();
    top_block->tb->start();
    std::cout << "Press Enter to quit: ";
    std::cin.ignore();
    top_block->tb->stop();
    top_block->tb->wait();

    return 0;
}
