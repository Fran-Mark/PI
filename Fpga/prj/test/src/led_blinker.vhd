------------------------------ Proyecto Integrador - IB ------------------------------
-- Test de Leds
-- Autor: Francisco Marquinez
-- Fecha: 6/12/21
----------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity led_blinker is
    generic(N : integer:=26);
    Port ( clk : in std_logic;
           syn_clr : in STD_LOGIC;
           leds : out std_logic_vector(3 downto 0);
           vadj_en : out std_logic
           );         
end led_blinker;

architecture Behavioral of led_blinker is
signal state_reg : unsigned (N-1 downto 0) := (others => '0');
signal state_next : unsigned (N-1 downto 0) := (others => '0');
signal max_tick : std_logic := '0';
signal toggle_buffer : std_logic  := '0';

begin
vadj_en <= '1';
state_next <= (others => '0') when syn_clr = '0' else
              state_reg + 1;

max_tick <= '1' when state_reg = 2**N-1 else
            '0';
                       
 process(clk)
   begin
      if (rising_edge (clk)) then
        if (syn_clr  = '0') then
         toggle_buffer <= '0';
         leds <= (others => '0');
        end if;
         state_reg <= state_next;
         if (max_tick = '1') then
            toggle_buffer  <= not toggle_buffer;
            
         end if;
         if (toggle_buffer = '1') then
            leds <= (others => '1');
         else 
            leds <= (others => '0');
         end if;
         
      end if;
      
 end process;
   


end Behavioral;
