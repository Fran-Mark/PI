#ifndef BEAMFORMER_HPP
#define BEAMFORMER_HPP
/********************
GNU Radio C++ Flow Graph Header File

Title: Beamformer
Author: fran
GNU Radio version: 3.8.4.0
********************/

/********************
** Create includes
********************/
#include <gnuradio/top_block.h>
#include <gnuradio/blocks/add_const_ff.h>
#include <gnuradio/blocks/deinterleave.h>
#include <gnuradio/blocks/file_sink.h>
#include <gnuradio/blocks/file_source.h>
#include <gnuradio/blocks/multiply_const.h>
#include <gnuradio/blocks/short_to_float.h>
#include <gnuradio/blocks/streams_to_vector.h>
#include <gnuradio/blocks/throttle.h>
#include <gnuradio/filter/hilbert_fc.h>



using namespace gr;


void BFmain(const char* fname);

class Beamformer {

private:


    filter::hilbert_fc::sptr hilbert_fc_0_0_1_0;
    filter::hilbert_fc::sptr hilbert_fc_0_0_1;
    filter::hilbert_fc::sptr hilbert_fc_0_0_0_0_0_0_1_0_0_0_0_0_0;
    filter::hilbert_fc::sptr hilbert_fc_0_0_0_0_0_0_1_0_0_0_0_0;
    filter::hilbert_fc::sptr hilbert_fc_0_0_0_0_0_0_1_0_0_0_0;
    filter::hilbert_fc::sptr hilbert_fc_0_0_0_0_0_0_1_0_0_0;
    filter::hilbert_fc::sptr hilbert_fc_0_0_0_0_0_0_1_0_0;
    filter::hilbert_fc::sptr hilbert_fc_0_0_0_0_0_0_1_0;
    filter::hilbert_fc::sptr hilbert_fc_0_0_0_0_0_0_1;
    filter::hilbert_fc::sptr hilbert_fc_0_0_0_0_0_0_0;
    filter::hilbert_fc::sptr hilbert_fc_0_0_0_0_0_0;
    filter::hilbert_fc::sptr hilbert_fc_0_0_0_0_0;
    filter::hilbert_fc::sptr hilbert_fc_0_0_0_0;
    filter::hilbert_fc::sptr hilbert_fc_0_0_0;
    filter::hilbert_fc::sptr hilbert_fc_0_0;
    filter::hilbert_fc::sptr hilbert_fc_0;
    blocks::throttle::sptr blocks_throttle_1;
    blocks::streams_to_vector::sptr blocks_streams_to_vector_0_1;
    blocks::short_to_float::sptr blocks_short_to_float_0_0;
    blocks::multiply_const_ff::sptr blocks_multiply_const_vxx_0_0;
    blocks::file_source::sptr blocks_file_source_0_0_1;
    blocks::file_sink::sptr blocks_file_sink_0;
    blocks::deinterleave::sptr blocks_deinterleave_0_0;
    blocks::add_const_ff::sptr blocks_add_const_vxx_0_0;


// Variables:
    int samp_rate = 32000;
    std::string filename;
public:
    top_block_sptr tb;
    Beamformer(const char* filename);
    ~Beamformer();

    int get_samp_rate () const;
    void set_samp_rate(int samp_rate);

};


#endif

