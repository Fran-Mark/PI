/* -*- c++ -*- */
/*
 * Copyright 2022 FranMark.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_BEAMFORMING_HEADERREADER_IMPL_H
#define INCLUDED_BEAMFORMING_HEADERREADER_IMPL_H

#include <beamforming/HeaderReader.h>

#define RDDATACOUNT_MASK ((1 << 12) - 1)
#define RDRSTBUSY_MASK  (1 << 12)
#define WRRSTBUSY_MASK  (1 << 13)
#define OVERFLOW_MASK   (1 << 14)
#define EMPTY_MASK      (1 << 15)
#define FULL_MASK       (1 << 16)
#define PROGFULL_MASK   (1 << 17)
#define PROGFULL_ASSERT ((1 << 16) - 1)

typedef struct
{
    bool full;
    bool empty;
    bool wr_rst_busy;
    bool rd_rst_busy;
    bool overflow;
    bool prog_full;
    uint32_t rd_data_count;
}fifo_flags_t;

//header size: 
typedef struct __attribute__((packed))
{
    uint64_t acq_timestamp_sec;
    uint64_t acq_timestamp_nsec;
    uint8_t bd_id;
    uint8_t ch_id;
    uint16_t ch_adc;
    uint8_t clk_divider;
    uint32_t fifo_flags[16];
    uint16_t payload_size;
    uint8_t padding; //padding to make the size of the struct to be a multiple of 8
}AcqPack_Header_t;

// converts FIFO flag register to FIFO flags structure
void fifoflags_reg_to_struct(fifo_flags_t* flags, uint32_t* flag_reg)
{
    flags->empty = *flag_reg & EMPTY_MASK;
    flags->full = *flag_reg & FULL_MASK;
    flags->overflow = *flag_reg & OVERFLOW_MASK;
    flags->rd_rst_busy = *flag_reg & RDRSTBUSY_MASK;
    flags->wr_rst_busy = *flag_reg & WRRSTBUSY_MASK;
    flags->prog_full = *flag_reg & PROGFULL_MASK;
    flags->rd_data_count = *flag_reg & RDDATACOUNT_MASK;
}

namespace gr {
  namespace beamforming {

    class HeaderReader_impl : public HeaderReader
    {
     private:
      // Nothing to declare in this block.

     public:
      HeaderReader_impl();
      ~HeaderReader_impl();

      // Where all the action really happens
      int work(
              int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items
      );
    };

  } // namespace beamforming
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_HEADERREADER_IMPL_H */

