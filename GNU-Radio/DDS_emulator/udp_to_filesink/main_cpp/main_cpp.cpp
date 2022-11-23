/********************
GNU Radio C++ Flow Graph Source File

Title: Not titled yet
Author: fran
GNU Radio version: v3.8.5.0-6-g57bd109d
********************/

#include "main_cpp.hpp"
using namespace gr;


main_cpp::main_cpp () {



    this->tb = gr::make_top_block("Not titled yet");


// Blocks:
    {
        this->blocks_udp_source_0 = blocks::udp_source::make(sizeof(short)*1, "192.168.0.21", 12345, 64088, true);
    }
    {
        this->blocks_file_sink_0 = blocks::file_sink::make(sizeof(short)*1, "/run/media/fran/46FAA90DFAA8FA77/Ventanas/IB/PI/GitHub/GNU-Radio/DDS_emulator/udp_to_filesink/ignore/contador", false);
    }

// Connections:
    this->tb->hier_block2::connect(this->blocks_udp_source_0, 0, this->blocks_file_sink_0, 0);
}

main_cpp::~main_cpp () {
}

// Callbacks:
int main_cpp::get_samp_rate () const {
    return this->samp_rate;
}

void main_cpp::set_samp_rate (int samp_rate) {
    this->samp_rate = samp_rate;
}


int main (int argc, char **argv) {

    main_cpp* top_block = new main_cpp();
    top_block->tb->start();
    std::cout << "Press Enter to quit: ";
    std::cin.ignore();
    top_block->tb->stop();
    top_block->tb->wait();

    return 0;
}
