#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "md5.h"

void print_hash(uint8_t *p){
    for(unsigned int i = 0; i < 16; ++i){
        printf("%02x", p[i]);
    }
    printf("\n");
}

int main(){
    uint8_t result[16];

    char* tested_string = "O poeta é um fingidor Finge tão completamente Que chega a fingir que é dor A dor que deveras sente.E os que lêem o que escreve, Na dor lida sentem bem, Não as duas que ele teve, Mas só a que eles não têm.E assim nas calhas de roda Gira, a entreter a razão, Esse comboio de corda Que se chama coração."; // Autopsicografia, Fernando Pessoa. 
    uint8_t  expected_hash[16] =  {0xf1, 0xd5, 0x93, 0x2c, 0x0c, 0x22, 0x27, 0x3a, 0x88, 0xaa, 0x76, 0xb0, 0xc3, 0xb0, 0xc2, 0xdf};

    md5String(tested_string, result);

    int boolean_is_correct = 1;
    for(unsigned int i = 0; i < 16; i++) {
        if(expected_hash[i] != result[i]){
            printf("O valor que diferenciou: %02x, %02x\n", expected_hash[i], result[i]);
            boolean_is_correct = 0;
        }
    }

    if(boolean_is_correct){
        printf("O valor está correto.\n");
        return 0;
    }else{
        printf("O valor está INCORRETO!.\n");
        return -1;
    }
}