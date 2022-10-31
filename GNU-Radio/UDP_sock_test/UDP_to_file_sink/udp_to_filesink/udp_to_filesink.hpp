#ifndef UDP_TO_FILESINK_HPP
#define UDP_TO_FILESINK_HPP
/********************
GNU Radio C++ Flow Graph Header File

Title: Not titled yet
Author: fran
GNU Radio version: v3.8.5.0-6-g57bd109d
********************/

/********************
** Create includes
********************/
#include <gnuradio/top_block.h>
#include <gnuradio/blocks/file_sink.h>
#include <gnuradio/blocks/udp_source.h>



using namespace gr;



class udp_to_filesink {

private:


    blocks::udp_source::sptr blocks_udp_source_0_0_0;
    blocks::file_sink::sptr blocks_file_sink_0;


// Variables:
    int samp_rate = 32000;

public:
    top_block_sptr tb;
    udp_to_filesink();
    ~udp_to_filesink();

    int get_samp_rate () const;
    void set_samp_rate(int samp_rate);

};


#endif

