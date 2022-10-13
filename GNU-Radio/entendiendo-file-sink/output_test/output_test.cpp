/********************
GNU Radio C++ Flow Graph Source File

Title: Entendiendo file sink
Author: fran
GNU Radio version: 3.8.4.0
********************/

#include "output_test.hpp"
using namespace gr;


output_test::output_test () {



    this->tb = gr::make_top_block("Entendiendo file sink");


// Blocks:
    {
        this->blocks_throttle_0 = blocks::throttle::make(sizeof(short)*1, samp_rate, true);
    }
    {
        this->blocks_short_to_float_0 = blocks::short_to_float::make(1, 1);
    }
    {
        this->blocks_float_to_complex_0 = blocks::float_to_complex::make(1);
    }
    {
        this->blocks_file_source_0 =blocks::file_source::make(sizeof(short)*1, "NotImplemented", true, 0, 0);
    }
    {
        this->blocks_file_sink_0 = blocks::file_sink::make(sizeof(gr_complex)*1, '/home/fran/Desktop/test1', false);
    }

// Connections:
    this->tb->hier_block2::connect(this->blocks_file_source_0, 0, this->blocks_throttle_0, 0);
    this->tb->hier_block2::connect(this->blocks_float_to_complex_0, 0, this->blocks_file_sink_0, 0);
    this->tb->hier_block2::connect(this->blocks_short_to_float_0, 0, this->blocks_float_to_complex_0, 0);
    this->tb->hier_block2::connect(this->blocks_throttle_0, 0, this->blocks_short_to_float_0, 0);
}

output_test::~output_test () {
}

// Callbacks:
int output_test::get_samp_rate () const {
    return this->samp_rate;
}

void output_test::set_samp_rate (int samp_rate) {
    this->samp_rate = samp_rate;
    this->blocks_throttle_0->set_sample_rate(this->samp_rate);
}


int main (int argc, char **argv) {

    output_test* top_block = new output_test();
    top_block->tb->start();
    std::cout << "Press Enter to quit: ";
    std::cin.ignore();
    top_block->tb->stop();
    top_block->tb->wait();

    return 0;
}
