library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity resizer is
    generic (INPUT_SIZE : integer := 8;
             OUTPUT_SIZE : integer := 8);
    port(
        data_in : in std_logic_vector(INPUT_SIZE-1 downto 0);
        data_out : out std_logic_vector(OUTPUT_SIZE-1 downto 0)
    );
end resizer;

architecture rtl of resizer is
begin
    data_out <= std_logic_vector(resize(signed(data_in), OUTPUT_SIZE));
end architecture rtl;
