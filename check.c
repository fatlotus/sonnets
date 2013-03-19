/*
 * This code was blatantly plagiarized from Wikipedia.
 * This comment has been added by SparkleShare!
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

uint32_t crc_table[256];

void make_crc_table(void) {
  for (uint32_t i = 0; i < 256; i++) {
    uint32_t c = i;
    for (int j = 0; j < 8; j++) {
      c = (c & 1) ? (0xEDB88320 ^ (c >> 1)) : (c >> 1);
    }
    crc_table[i] = c;
  }
}
 
uint32_t crc32stdin() {
  uint32_t c = 0xFFFFFFFF;
  char ch;
    
  for (;;) {
    ch = getchar();
    if (ch < 0) break;
    c = crc_table[(c ^ ch) & 0xFF] ^ (c >> 8);
  }
    
  return c ^ 0xFFFFFFFF;
}

int main(int argc, char ** argv) {
  make_crc_table();
  
  printf("0x%08x\n", crc32stdin());
  
  return 0;
};