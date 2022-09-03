----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 11/29/2021 11:16:37 PM
-- Design Name: 
-- Module Name: contador_test - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity contador_test is
--  Port ( );
end contador_test;

architecture Behavioral of contador_test is
    constant N: integer := 8;
    constant LED_COUNT : integer :=4;
    constant T : time := 10 ns; -- El clock va a 100 MHz
    
    --Entradas
    signal clk : std_logic := '0';
    signal syn_clr : std_logic := '0';
    signal load_en : std_logic := '0';
    signal load_val : unsigned (LED_COUNT -1 downto 0) := (others => '0');
    signal en : std_logic := '0';
    signal up : std_logic := '0';         
          
    -- Salidas
    signal current_val : std_logic_vector (LED_COUNT-1 downto 0);
    
begin
    uut : entity Work.contador(Behavioral)
        generic map (
            N => N
        )
        port map(
            clk => clk,
            syn_clr => syn_clr,
            load_en => load_en,
            load_val => load_val,
            en => en,
            up => up,
            current_val => current_val
        );
    
    --Genero clock de 100 MHz
    clk_process: process
    begin
        clk <= '0';
        wait for T/2;
        clk <= '1';
        wait for T/2;
    end process;


    stim_proc: process
    begin
        syn_clr <= '1';
        wait for 3*T;
        syn_clr <= '0';
        wait until rising_edge(clk);
        wait for 2 ps;
        -------------- Contador hacia arriba --------------
        en <= '1';
        up <= '1';
        wait for 4*T;
        for j in 0 to 9 loop
            for i in 0 to 2**N - 1 loop            
                wait until falling_edge(clk);
            end loop;
            assert unsigned(current_val) - 1   = to_unsigned(j, LED_COUNT) report "Mal el contador hacia arriba en la iteración " & integer'image(j) severity failure;
        end loop;
        
        syn_clr <= '1';
        wait for 3*T;
        syn_clr <= '0';
        wait until rising_edge(clk);

        
         -------------- Contador usando load --------------
        load_en <= '1';
        load_val <= "0101";   
        wait for 3*T;     
        wait until falling_edge(clk);
        assert unsigned(current_val) = unsigned(load_val) report "No anda el load" severity failure;
        load_en <= '0';        

        
         assert false report "Todo salió bien! :D" severity FAILURE;
    end process;
end Behavioral;
