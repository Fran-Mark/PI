#ifndef OUTPUT_TEST_HPP
#define OUTPUT_TEST_HPP
/********************
GNU Radio C++ Flow Graph Header File

Title: Entendiendo file sink
Author: fran
GNU Radio version: 3.8.4.0
********************/

/********************
** Create includes
********************/
#include <gnuradio/top_block.h>
#include <gnuradio/blocks/file_sink.h>
#include <gnuradio/blocks/file_source.h>
#include <gnuradio/blocks/float_to_complex.h>
#include <gnuradio/blocks/short_to_float.h>
#include <gnuradio/blocks/throttle.h>



using namespace gr;



class output_test {

private:


    blocks::throttle::sptr blocks_throttle_0;
    blocks::short_to_float::sptr blocks_short_to_float_0;
    blocks::float_to_complex::sptr blocks_float_to_complex_0;
    blocks::file_source::sptr blocks_file_source_0;
    blocks::file_sink::sptr blocks_file_sink_0;


// Variables:
    int samp_rate = 32000;

public:
    top_block_sptr tb;
    output_test();
    ~output_test();

    int get_samp_rate () const;
    void set_samp_rate(int samp_rate);

};


#endif

