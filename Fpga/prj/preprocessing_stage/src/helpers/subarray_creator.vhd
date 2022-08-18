library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;

entity subarray_creator is
  generic (
    INPUT_WIDTH  : natural := 32;
    OFFSET       : natural := 0;
    OUTPUT_WIDTH : natural := 32);

  port (
    tdata_in   : in std_logic_vector(INPUT_WIDTH - 1 downto 0);
    tvalid_in  : in std_logic;
    tdata_out  : out std_logic_vector(OUTPUT_WIDTH - 1 downto 0);
    tvalid_out : out std_logic
  );
end subarray_creator;

architecture rtl of subarray_creator is
begin
  tdata_out <= tdata_in(OFFSET + OUTPUT_WIDTH - 1 downto OFFSET);
  tvalid_out <= tvalid_in;
end rtl;
