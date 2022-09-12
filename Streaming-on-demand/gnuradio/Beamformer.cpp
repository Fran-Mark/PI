/********************
GNU Radio C++ Flow Graph Source File

Title: Beamformer
Author: fran
GNU Radio version: 3.8.4.0
********************/

#include "Beamformer.hpp"
using namespace gr;



Beamformer::Beamformer (const char* fname)
    :filename(fname)
{



    this->tb = gr::make_top_block("Beamformer");


// Blocks:
    {
        this->hilbert_fc_0_0_1_0 = filter::hilbert_fc::make(
            16*4,
            gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->hilbert_fc_0_0_1 = filter::hilbert_fc::make(
            16*4,
            gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->hilbert_fc_0_0_0_0_0_0_1_0_0_0_0_0_0 = filter::hilbert_fc::make(
            16*4,
            gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->hilbert_fc_0_0_0_0_0_0_1_0_0_0_0_0 = filter::hilbert_fc::make(
            16*4,
            gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->hilbert_fc_0_0_0_0_0_0_1_0_0_0_0 = filter::hilbert_fc::make(
            16*4,
            gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->hilbert_fc_0_0_0_0_0_0_1_0_0_0 = filter::hilbert_fc::make(
            16*4,
            gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->hilbert_fc_0_0_0_0_0_0_1_0_0 = filter::hilbert_fc::make(
            16*4,
            gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->hilbert_fc_0_0_0_0_0_0_1_0 = filter::hilbert_fc::make(
            16*4,
            gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->hilbert_fc_0_0_0_0_0_0_1 = filter::hilbert_fc::make(
            16*4,
            gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->hilbert_fc_0_0_0_0_0_0_0 = filter::hilbert_fc::make(
            16*4,
            gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->hilbert_fc_0_0_0_0_0_0 = filter::hilbert_fc::make(
            16*4,
            gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->hilbert_fc_0_0_0_0_0 = filter::hilbert_fc::make(
            16*4,
           gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->hilbert_fc_0_0_0_0 = filter::hilbert_fc::make(
            16*4,
           gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->hilbert_fc_0_0_0 = filter::hilbert_fc::make(
            16*4,
           gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->hilbert_fc_0_0 = filter::hilbert_fc::make(
            16*4,
           gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->hilbert_fc_0 = filter::hilbert_fc::make(
            16*4,
           gr::fft::window::WIN_HAMMING,
            6.76);
    }
    {
        this->blocks_throttle_1 = blocks::throttle::make(sizeof(short)*1, samp_rate, true);
    }
    {
        this->blocks_streams_to_vector_0_1 = blocks::streams_to_vector::make(sizeof(gr_complex)*1, 16);
    }
    {
        this->blocks_short_to_float_0_0 = blocks::short_to_float::make(1, 1);
    }
    {
        this->blocks_multiply_const_vxx_0_0 = blocks::multiply_const_ff::make(2.0/8192.0);
    }
    {
        this->blocks_file_source_0_0_1 =blocks::file_source::make(sizeof(short)*1, "../test_data/test_data.npy", true, 64, 0);
    }
    {
        this->blocks_file_sink_0 = blocks::file_sink::make(sizeof(gr_complex)*16, filename.c_str(), false);
    }
    {
        this->blocks_deinterleave_0_0 = blocks::deinterleave::make(sizeof(float)*1, 1);
    }
    {
        this->blocks_add_const_vxx_0_0 = blocks::add_const_ff::make(-8191.5);
    }

// Connections:
    this->tb->hier_block2::connect(this->blocks_add_const_vxx_0_0, 0, this->blocks_multiply_const_vxx_0_0, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 0, this->hilbert_fc_0, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 5, this->hilbert_fc_0_0, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 4, this->hilbert_fc_0_0_0, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 3, this->hilbert_fc_0_0_0_0, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 2, this->hilbert_fc_0_0_0_0_0, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 13, this->hilbert_fc_0_0_0_0_0_0, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 1, this->hilbert_fc_0_0_0_0_0_0_0, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 8, this->hilbert_fc_0_0_0_0_0_0_1, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 9, this->hilbert_fc_0_0_0_0_0_0_1_0, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 10, this->hilbert_fc_0_0_0_0_0_0_1_0_0, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 11, this->hilbert_fc_0_0_0_0_0_0_1_0_0_0, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 15, this->hilbert_fc_0_0_0_0_0_0_1_0_0_0_0, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 12, this->hilbert_fc_0_0_0_0_0_0_1_0_0_0_0_0, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 14, this->hilbert_fc_0_0_0_0_0_0_1_0_0_0_0_0_0, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 6, this->hilbert_fc_0_0_1, 0);
    this->tb->hier_block2::connect(this->blocks_deinterleave_0_0, 7, this->hilbert_fc_0_0_1_0, 0);
    this->tb->hier_block2::connect(this->blocks_file_source_0_0_1, 0, this->blocks_throttle_1, 0);
    this->tb->hier_block2::connect(this->blocks_multiply_const_vxx_0_0, 0, this->blocks_deinterleave_0_0, 0);
    this->tb->hier_block2::connect(this->blocks_short_to_float_0_0, 0, this->blocks_add_const_vxx_0_0, 0);
    this->tb->hier_block2::connect(this->blocks_streams_to_vector_0_1, 0, this->blocks_file_sink_0, 0);
    this->tb->hier_block2::connect(this->blocks_throttle_1, 0, this->blocks_short_to_float_0_0, 0);
    this->tb->hier_block2::connect(this->hilbert_fc_0, 0, this->blocks_streams_to_vector_0_1, 0);
    this->tb->hier_block2::connect(this->hilbert_fc_0_0, 0, this->blocks_streams_to_vector_0_1, 5);
    this->tb->hier_block2::connect(this->hilbert_fc_0_0_0, 0, this->blocks_streams_to_vector_0_1, 4);
    this->tb->hier_block2::connect(this->hilbert_fc_0_0_0_0, 0, this->blocks_streams_to_vector_0_1, 3);
    this->tb->hier_block2::connect(this->hilbert_fc_0_0_0_0_0, 0, this->blocks_streams_to_vector_0_1, 2);
    this->tb->hier_block2::connect(this->hilbert_fc_0_0_0_0_0_0, 0, this->blocks_streams_to_vector_0_1, 13);
    this->tb->hier_block2::connect(this->hilbert_fc_0_0_0_0_0_0_0, 0, this->blocks_streams_to_vector_0_1, 1);
    this->tb->hier_block2::connect(this->hilbert_fc_0_0_0_0_0_0_1, 0, this->blocks_streams_to_vector_0_1, 8);
    this->tb->hier_block2::connect(this->hilbert_fc_0_0_0_0_0_0_1_0, 0, this->blocks_streams_to_vector_0_1, 9);
    this->tb->hier_block2::connect(this->hilbert_fc_0_0_0_0_0_0_1_0_0, 0, this->blocks_streams_to_vector_0_1, 10);
    this->tb->hier_block2::connect(this->hilbert_fc_0_0_0_0_0_0_1_0_0_0, 0, this->blocks_streams_to_vector_0_1, 11);
    this->tb->hier_block2::connect(this->hilbert_fc_0_0_0_0_0_0_1_0_0_0_0, 0, this->blocks_streams_to_vector_0_1, 15);
    this->tb->hier_block2::connect(this->hilbert_fc_0_0_0_0_0_0_1_0_0_0_0_0, 0, this->blocks_streams_to_vector_0_1, 12);
    this->tb->hier_block2::connect(this->hilbert_fc_0_0_0_0_0_0_1_0_0_0_0_0_0, 0, this->blocks_streams_to_vector_0_1, 14);
    this->tb->hier_block2::connect(this->hilbert_fc_0_0_1, 0, this->blocks_streams_to_vector_0_1, 6);
    this->tb->hier_block2::connect(this->hilbert_fc_0_0_1_0, 0, this->blocks_streams_to_vector_0_1, 7);
}

Beamformer::~Beamformer () {
}

// Callbacks:
int Beamformer::get_samp_rate () const {
    return this->samp_rate;
}

void Beamformer::set_samp_rate (int samp_rate) {
    this->samp_rate = samp_rate;
    this->blocks_throttle_1->set_sample_rate(this->samp_rate);
}


void BFmain (const char* filename) {
    Beamformer* top_block = new Beamformer(filename);
    top_block->tb->start();
    std::cout << "Init\n";
    //sleep for 5 secs
    sleep(5);
    std::cout << "Bye\n";
    top_block->tb->stop();
    top_block->tb->wait();
}

// int main (int argc, char **argv) {
//     BFmain(argv[1]);
//     return 0;
// }
