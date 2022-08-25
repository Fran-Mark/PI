library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity complex_splitter is
    generic (INPUT_SIZE : integer := 8
             );
    port(
        data_in : in std_logic_vector(INPUT_SIZE-1 downto 0);
        data_re_out : out std_logic_vector(INPUT_SIZE/2 -1 downto 0);
        data_im_out : out std_logic_vector(INPUT_SIZE/2 -1 downto 0)
    );
end complex_splitter   ;

architecture rtl of complex_splitter    is
begin
    data_re_out <= data_in(INPUT_SIZE/2-1 downto 0);
    data_im_out <= data_in(INPUT_SIZE - 1 downto INPUT_SIZE/2);
end rtl;
