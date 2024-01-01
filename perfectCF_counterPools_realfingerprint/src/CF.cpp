#include "CF.hpp"
#include "utils.h"
#include "crc.h"
#include "xxhash.h"
#include "murmur3.h"
#include <stdio.h>
#include <functional>
#include <cstring>
#include <smmintrin.h>
#include <iostream>
#include <stdlib.h>
#include <random>
#include <chrono>
#include <math.h>
#include <fstream>
#include <assert.h>
#include <time.h>
#include <algorithm>
#include <cinttypes>
#include <immintrin.h>





template <typename T>  
uint64 CityHash(T key, uint64_t seed) 
{
    char* k= (char*) malloc(sizeof(T));
    k = (char*) memcpy(k,&key,sizeof(T));
    uint64 r= CityHash64WithSeed(k,sizeof(T),seed);
    free(k);
    return r;
}

template <typename T>  
uint64 XXHash(T key, uint64_t seed) 
{
    char* k= (char*) malloc(sizeof(T));
    k = (char*) memcpy(k,&key,sizeof(T));

    XXH64_hash_t r=XXH64(k,sizeof(T),seed);
    free(k);
    return (uint64) r;
}

template <typename T>  
uint32_t CRC24Hash(T key) 
{
    uint8_t* k= (uint8_t*) malloc(sizeof(T));
    k = (uint8_t*) memcpy(k,&key,sizeof(T));

    uint32_t r=crc24(k,sizeof(T));
    free(k);
    return (uint32_t) r;
}

	template <typename T>  
uint32_t CRC32Hash(T key, uint32_t seed) 
{
    char* k= (char*) malloc(sizeof(T));
    k = (char*) memcpy(k,&key,sizeof(T));

    uint32_t r=crc32(k,sizeof(T),seed);
    free(k);
    return (uint32_t) r;
}

template <typename T>  
uint64 MurMurHash(T key, uint64_t seed) 
{
    char* k= (char*) malloc(sizeof(T));
    k = (char*) memcpy(k,&key,sizeof(T));
    uint32_t r;
    MurmurHash3_x86_32(k,sizeof(T),seed,&r);
    free(k);
    return r;
}

template <typename T>  
uint32_t NOHash(T key) 
{
    uint8_t* k= (uint8_t*) malloc(sizeof(T));
    k = (uint8_t*) memcpy(k,&key,sizeof(T));

    uint32_t r=k[1]+256*(k[2]+256*k[0]); 
    free(k);
    return (uint32_t) r;
}

template <typename key_type> 
int CF<key_type>::myhash(key_type key, int i, int s) {
    uint64_t   val=0;

    if (hash_type==0)
	    val = CRC32Hash<key_type>(key,444);
    if (hash_type==1)
	    val = MurMurHash<key_type>(key,2137);
    if (hash_type==2)
	    val = XXHash<key_type>(key,2137);
    if (hash_type==3)
	    val = CityHash<key_type>(key,2137);
    if (hash_type==4)
	    val = CRC24Hash<key_type>(key);
    if (hash_type==5)
	    val = NOHash<key_type>(key);
    
    if (i==1) { //fingerprint
    	return (val %s);
    }
    if (i==2) { //pointer
	val = (val / fp_size);     
    	return (val %s);
    }
    if (i==3) { //pointer 2
    	val = XXHash<key_type>(key,2314);
        return (val % s);
    }
    return -1;
}

/*
 * Constructor
 */


extern int verbose; // define the debug level

template <typename key_type>
CF<key_type>::CF(int M,int f, int slot, int hash_type_param)
{
  initLookupTableFunc();
  cf_size=M;
  fp_size=(1<<f);
  num_slots=slot;
  hash_type=hash_type_param;
  if (cf_size>0) {
      keys = new key_type*[M];
      table = new int*[M];
      table_bit = new int*[M];
      

      for (int i = 0;  i < M;  i++) {
	      keys[i]= new key_type[num_slots]; 
	      table[i]= new int[num_slots]; 
	      table_bit[i]=new int[num_slots]; 
        
      }


      m_pools = new uint64_t[M];
      m_encodings = new uint16_t[M];

      clear();
  }
}

/*
 * Distructor
 */
template <typename key_type>
CF<key_type>::~CF()
{
  if (cf_size>0) {
	for (int i = 0;  i < cf_size;  i++) {delete[] table[i]; delete[] table_bit[i];}
	delete[] table;
	delete[] table_bit;
	delete[] m_pools;
	delete[] m_encodings;
  }
}

//DUMP
template <typename key_type>
void CF<key_type>::dump()
{
  if (cf_size>0) {
	for(int i=0; i<cf_size; i++) {
	    for(int ii=0; ii<4; ii++) {
		printf("table[%d][%d] = %d %d\n", i,ii, table[i][ii], table_bit[i][ii]);
	}
	}
  }
}

/*
 * Clear
 */

template <typename key_type>
void CF<key_type>::clear()
{
	num_item=0; num_access=0;
	victim_fingerprint=-9;
	victim_pointer=-1;
  if (cf_size>0) {
	for(int i=0; i<cf_size; i++) {
      m_pools[i] = 0;
      uint8_t sizes_array[4] = { 0,0,0,64 };
      uint32_t new_sizes = 0;
      int k = 4;
      for (int i = 0; i < k - 1; ++i)
      {
        new_sizes |= sizes_array[i];
        new_sizes <<= 8;
      }
      new_sizes |= sizes_array[k - 1];

      uint16_t &pool_encoding = m_encodings[i];
      pool_encoding = encode_without_auxilary_map(new_sizes);





	    for(int ii=0; ii<4; ii++) {
		    table[i][ii]=-1;
		    table_bit[i][ii]=-10;
	    }
    }
  }
}







template <typename key_type>
void CF<key_type>::initLookupTableFunc()
{
	if (m_initLookupTable)
	{
		return;
	}
	m_initLookupTable = true;

	/*
	X = sum(seq) + 2
	Y = len(seq)
	SABsumDict = dict([((n, x, y), sum([nSAB(n - _, y) for _ in range(x)])) for n in range(X) for x in range(X) for y in range(Y)])
	*/

	uint64_t X = 66; 
	uint64_t Y = 4;

	for (uint64_t n = 0; n < X; ++n)
	{
		for (uint64_t x = 0; x < X; ++x)
		{
			for (uint64_t y = 1; y < Y; ++y)
			{
				uint64_t res = 0;
				for (uint64_t u = 0; u < x; ++u)
				{
					res += starsAndBars(n - u, y);
				}
				uint64_t key = ((n << 32) | (x << 16) | y);
				m_auxilary_map[key] = res;
			}
		}
	}

	for (uint16_t encoding = 0; encoding < STARS_AND_BARS_64_4; ++encoding)
	{
		m_lookup[encoding] = decode_offsets(encoding, 64, 4);
	}

	// comment out for testing at constructor
	m_auxilary_map.clear();
}

template <typename key_type>
uint32_t CF<key_type>::decode_sizes(uint16_t encoding, uint64_t n, uint64_t k)
{
	/*
	def SABdecode(conf,n,k):
		if k == 1:
			return [n]
		f = 0
		while SABsumDict[(n,f+1,k-1)] <= conf:
			f += 1
		return [f] + SABdecode(conf-SABsumDict[(n,f,k-1)],n-f,k-1)
	*/

	if (k == 1)
	{
		return n;
	}

	uint64_t f = 0;
	while (m_auxilary_map[CONCAT_KEYS(n, f + 1, k - 1)] <= encoding)
	{
		++f;
	}

	return (f << (8 * (k - 1))) | decode_sizes(encoding - m_auxilary_map[CONCAT_KEYS(n, f, k - 1)], n - f, k - 1);
}

template <typename key_type>
uint32_t CF<key_type>::decode_offsets(uint16_t encoding, uint64_t n, uint64_t k)
{
	uint32_t sizes = decode_sizes(encoding, n, k);
	uint8_t* sizes_array = (uint8_t*)&sizes;
	uint32_t offsets = 0;
	uint32_t offset = sizes_array[k - 1];

	for (int i = 1; i < k - 1; ++i)
	{
		offsets |= offset;
		offsets <<= 8;
		offset += sizes_array[k - 1 - i];
	}
	offsets |= offset;

	uint8_t* offsets_array = (uint8_t*)&offsets;
	std::reverse(offsets_array, offsets_array + k);
	return offsets;
}

template <typename key_type>
uint16_t CF<key_type>::encode(uint32_t sizes)
{
	uint64_t n = 64;
	uint64_t k = 4;
	uint16_t encoding = 0;
	for (int i = 0; i < k - 1; ++i)
	{
		uint64_t size = ((sizes & (0xFF << ((k - i - 1) << 3))) >> ((k - i - 1) << 3));
		encoding += m_auxilary_map[CONCAT_KEYS(n, size, k - i - 1)];
		n -= size;
	}
	return encoding;
}

template <typename key_type>
uint16_t CF<key_type>::encode_without_auxilary_map(uint32_t sizes)
{
	uint64_t n = 64;
	uint64_t k = 4;

	uint16_t encoding = 0;
	for (int i = 0; i < k - 1; ++i)
	{
		uint64_t size = ((sizes & (0xFF << ((k - i - 1) << 3))) >> ((k - i - 1) << 3));

		uint64_t res = 0;
		for (uint64_t u = 0; u < size; ++u)
		{
			res += starsAndBars(n - u, k - i - 1);
		}
		encoding += res;

		n -= size;
	}

	return encoding;
}







template <typename key_type>
bool CF<key_type>::incPool(int index, int counterNum , uint64_t value){

  // check if there is enough space in the pool
  int k=4;
  uint8_t* offsets = (uint8_t*)(m_lookup + m_encodings[index]);
  uint64_t &pool = m_pools[index];

  uint64_t oldVal = getVal(index, counterNum);

  // TODO optimize ///////////////////////////////////////
  //int newSizeBits = floor(log2(value+oldVal)) + 1;

  // TODO check
  int newSizeBits = 64 - __builtin_clz(value + oldVal);

  int bitsSizeDiff;
  if(counterNum < 3){
    int oldSizeBits = offsets[counterNum + 1] - offsets[counterNum];
    bitsSizeDiff  = newSizeBits - oldSizeBits;

    //check if the last counter will have enough space
    int lastCounterOldBitSize = (64 - offsets[k-1]);
    int lastCounterNewBitSize = lastCounterOldBitSize - bitsSizeDiff;
    int lastCounterVal = getVal(index, k-1);

    // the min bitSize needed for this val is ( TODO optimize)
    int lastCounterMinBitSize = floor(log2(lastCounterVal)) + 1;

    // if the new bit size smaller than the min then return false
    if(  lastCounterNewBitSize < lastCounterMinBitSize ){
      return false;
    }
  }
  else{
    int oldSizeBits = 64 - offsets[counterNum];
    if(oldSizeBits < newSizeBits){
      return false;
    }
    bitsSizeDiff = 0;
  }
  


  

  ////////////// debuging //////////////
  // value = 2;
  // index = 2;
  // counterNum = 3;
  // uint64_t a =  getVal(index, counterNum);
  // printf("%" PRIu64 "\n", a);
  //////////////////////////////////////


  // // TODO: optimize to one call
  //  for(int i=0; i< 4;i++){
  //    printf("loop\n");
  //    incPoolCounter(index, counterNum , 1);
  //    printf("\n\n");
  //  }

// incPoolCounter(index, 0 , 1, 1);
// incPoolCounter(index, 1 , 1, 1);
// incPoolCounter(index, 2 , 1, 1);
// incPoolCounter(index, 3 , 1, 1);

// incPoolCounter(index, 1 , 7, 3);
// incPoolCounter(index, 2 , 2, 1);


incPoolCounter(index, counterNum, value, bitsSizeDiff);

  ////////////// debuging check ////////
   //printf("0: %d\n",getVal(index, 0));
   //printf("1: %d\n",getVal(index, 1));
   //printf("2: %d\n",getVal(index, 2));
   //printf("3: %d\n",getVal(index, 3));
  //////////////////////////////////////



  return true;
}










// called only if already checked that there is enough space to inc the counter
template <typename key_type>
void CF<key_type>::incPoolCounter(int index, int counterNum, int incVal, int bitDiff){

  uint64_t &pool = m_pools[index];
  uint8_t* offsets = (uint8_t*)(m_lookup + m_encodings[index]);
  uint64_t k = 4;

  int counterBitOffset = offsets[counterNum];

  
  int counterBitSize;
  uint64_t mask;
  uint64_t counterVal = pool >> counterBitOffset;
  

  if (counterNum < 3)
  {
    counterBitSize = offsets[counterNum + 1] - counterBitOffset;
    mask = (((uint64_t)1 << (counterBitSize)) - 1);
    counterVal &= mask;

    if (counterVal + incVal <= mask)
    {
      pool += ((uint64_t)incVal << counterBitOffset);
      return;
    }
  }
  else
  {
    counterBitSize = 64 - counterBitOffset;

    if (counterVal + incVal < ((uint64_t)1 << counterBitSize))
    {
      pool += ((uint64_t)incVal << counterBitOffset);
      return;
    }
    else if (counterBitSize == 64)
    {
      pool+=incVal;
      return;
    }
  }





  // if we reach here then we need to arrange the pool before we can inc the counter 
  uint8_t sizes_array[4] = { 0 };
  sizes_array[0] = offsets[1];
  for (int i = 1; i < k - 1; ++i)
  {
    sizes_array[i] = offsets[i + 1] - offsets[i];
  }
  sizes_array[k - 1] = 64 - offsets[k - 1];

  sizes_array[counterNum]+=bitDiff;
  sizes_array[k - 1]-=bitDiff;

  uint32_t new_sizes = 0;
  for (int i = 0; i < k - 1; ++i)
  {
    new_sizes |= sizes_array[i];
    new_sizes <<= 8;
  }
  new_sizes |= sizes_array[k - 1];

  uint16_t &pool_encoding = m_encodings[index];
  pool_encoding = encode_without_auxilary_map(new_sizes);

  uint64_t pool_lsb = pool & (((uint64_t)1 << (counterBitOffset + counterBitSize)) - 1);
  uint64_t pool_msb = pool & (~(((uint64_t)1 << (counterBitOffset + counterBitSize)) - 1));
  pool = pool_lsb | (pool_msb << bitDiff);

  counterBitSize += bitDiff;

  if (counterVal + incVal < ((uint64_t)1 << counterBitSize))
  {
    pool += ((uint64_t)incVal << counterBitOffset);
  }
  else
  {
    pool+= incVal;
  }
}






template <typename key_type>
uint64_t CF<key_type>::getVal(int index, int counterNum){

  uint64_t &pool = m_pools[index];

  uint8_t* offsets = (uint8_t*)(m_lookup + m_encodings[index]);
  int counterBitOffset = offsets[counterNum];

  uint64_t mask;
  uint64_t value = pool >> counterBitOffset;  
  int counterBitSize;
  if (counterNum < 3)
  {
    counterBitSize = offsets[counterNum + 1] - counterBitOffset;
    mask = (((uint64_t)1 << (counterBitSize)) - 1);
    value &= mask;
  }
  return value;
}





template <typename key_type>
uint64_t CF<key_type>::delCounter(int index, int counterNum){

  uint16_t &pool_encoding = m_encodings[index];
  uint64_t &pool = m_pools[index];


  uint8_t* offsets = (uint8_t*)(m_lookup + pool_encoding);
  uint64_t k = 4;

  int counterBitOffset = offsets[counterNum];

  uint64_t mask;
  uint64_t value = pool >> counterBitOffset;  
  int counterBitSize;
  if (counterNum < 3)
  {
    counterBitSize = offsets[counterNum + 1] - counterBitOffset;
    mask = (((uint64_t)1 << (counterBitSize)) - 1);
    value &= mask;
  }
  else
  {
    counterBitSize = 64 - counterBitOffset;
  }

  // delete counter  TODO: double check
  uint64_t pool_lsb = pool & (((uint64_t)1 << (counterBitOffset)) - 1);
  uint64_t pool_msb = pool & (~(((uint64_t)1 << (counterBitOffset + counterBitSize)) - 1));
  pool = pool_lsb | (pool_msb << 1);


  // update encoding
  uint8_t sizes_array[4] = { 0 };
  sizes_array[0] = offsets[1];
  for (int i = 1; i < k - 1; ++i)
  {
    sizes_array[i] = offsets[i + 1] - offsets[i];
  }
  sizes_array[k - 1] = 64 - offsets[k - 1];

  int tmp = sizes_array[counterNum];
  sizes_array[counterNum] = 0;
  sizes_array[k - 1] += tmp;

  uint32_t new_sizes = 0;
  for (int i = 0; i < k - 1; ++i)
  {
    new_sizes |= sizes_array[i];
    new_sizes <<= 8;
  }
  new_sizes |= sizes_array[k - 1];
  pool_encoding = encode_without_auxilary_map(new_sizes);
  return value;
}






/*
 * Insert
 */
template <typename key_type>
bool CF<key_type>::insert(key_type key)
{
  if (cf_size==0) return true;
  //if (query(key)) return true;
  int fingerprint=myhash(key,1,fp_size);
  int p=myhash(key,2,cf_size);
  p=p % cf_size;
  return insert2(key,p,fingerprint);
}




template <typename key_type>
bool CF<key_type>::insert2(key_type key,int p,int fingerprint)
{
table[0][1] = 0;
  __m128i bin1Content = *((__m128i*) table[0]);
  __m128i bin2Content = *((__m128i*) table[1]);

  __m256i binContent = _mm256_set_m128i(bin2Content, bin1Content);



/////////////////////////////////////////////////////////////////////////////////////////
__m128i a = _mm256_extracti128_si256(binContent, 0);
cout << "table="<<_mm_extract_epi32(a, 0)<<" "<<_mm_extract_epi32(a, 1)<<" "<<_mm_extract_epi32(a, 2)<<" "<<_mm_extract_epi32(a, 3)<<"||";
a = _mm256_extracti128_si256(binContent, 1);
cout << " "<<_mm_extract_epi32(a, 0)<<" "<<_mm_extract_epi32(a, 1)<<" "<<_mm_extract_epi32(a, 2)<<" "<<_mm_extract_epi32(a, 3)<<endl;

/////////////////////////////////////////////////////////////////////////////////////////


  __m256i item = _mm256_set1_epi32((int)(0));

  const __m256i match1 = _mm256_cmpeq_epi32(item, binContent);
  const int mask1 = _mm256_movemask_epi8(match1) & 0xffff;
  cout << "mask: "<<mask1<<endl;
  if (mask1 != 0) {
    int tz1 = _tzcnt_u32(mask1);
    cout << "tz:" <<tz1 << endl;
  }




  return true;
  int t;
  int new_bit=0;
  int old_bit=0;
  int value = 1;

  int newf=-1;
  key_type new_key;
  uint64_t val;

  if (cf_size==0) return true;
  for (t = 1;  t <= 1000;  t++) {
    p=p % cf_size;
    int p1=p^myhash(fingerprint,3,1<<30);
	  p1=p1 % cf_size;




      // printf("====== %d  %d\n",table[p],table[p1]);
      // while(true){
      // }
    cout << "finger"<<fingerprint<<endl;

    cout << "bin1="<<table[p][0]<<" "<<table[p][1]<<" "<<table[p][2]<<" "<<table[p][3]<<endl;


    // check if the fingerprint exist in one of the two pinss
    const __m256i item1 = _mm256_set1_epi32((int)fingerprint);
    __m128i bin1Content = *((__m128i*) table[p]);
    
    
    cout << "bin1_xv2="<<_mm_extract_epi32(bin1Content, 0)<<" "<<_mm_extract_epi32(bin1Content, 1)<<" "<<_mm_extract_epi32(bin1Content, 2)<<" "<<_mm_extract_epi32(bin1Content, 3)<<endl;


    __m128i bin2Content = *((__m128i*) table[p1]);
    __m256i binsContent = _mm256_set_m128i(bin2Content, bin1Content);


    ///////////////////////////////////////
    __m128i a = _mm256_extracti128_si256(binsContent, 0);
    cout << "bin1_xv3="<<_mm_extract_epi32(a, 0)<<" "<<_mm_extract_epi32(a, 1)<<" "<<_mm_extract_epi32(a, 2)<<" "<<_mm_extract_epi32(a, 3)<<"||";
    a = _mm256_extracti128_si256(binsContent, 1);
    cout << " "<<_mm_extract_epi32(a, 0)<<" "<<_mm_extract_epi32(a, 1)<<" "<<_mm_extract_epi32(a, 2)<<" "<<_mm_extract_epi32(a, 3)<<endl;

    ////////////////////////////////////


    const __m256i match1 = _mm256_cmpeq_epi32(item1, binsContent);
	  const int mask1 = _mm256_movemask_epi8(match1) & 0xffff;
    cout << mask1<<endl;
    if (mask1 != 0) {
      cout << "innnn" <<endl;
      int tz1 = _tzcnt_u32(mask1);
      cout << "tz:" <<tz1 << endl;
      cout << "p:" <<p << endl;
      int rowIndex = (tz1 < 3) ? p : p1;
      int counterNum = tz1 & 3;

      cout << "inc= row:" << rowIndex << " counter:" << counterNum << " val:"<<value<<endl;

        ////////////// debuging check ////////
   printf("0: %d\n",getVal(p, 0));
   printf("1: %d\n",getVal(p, 1));
   printf("2: %d\n",getVal(p, 2));
   printf("3: %d\n",getVal(p, 3));
   printf("\n");
  //////////////////////////////////////
      
      if(incPool(rowIndex, counterNum,value)){


          ////////////// debuging check ////////
   printf("0: %d\n",getVal(p, 0));
   printf("1: %d\n",getVal(p, 1));
   printf("2: %d\n",getVal(p, 2));
   printf("3: %d\n",getVal(p, 3));
  //////////////////////////////////////
        
        num_item++;
        table_bit[rowIndex][counterNum]=  (tz1 < 3) ? new_bit : ((1+new_bit)%2);
        // printf(" @@@@@@@@ inserted in table[%d][%d] f=%u\n",rowIndex,counterNum,fingerprint);
        // while(true){
        // }
        return true;
      }
      else{
        table[rowIndex][counterNum] = -1;
        value += delCounter(rowIndex, counterNum);
        continue;
      }
    }

    // check if there is an empty spot in one of the two pins
    __m256i item2 = _mm256_set1_epi32((int)(-1));
    __m128i b = _mm256_extracti128_si256(item2, 0);
    cout << "bin1_xv-1="<<_mm_extract_epi32(b, 0)<<" "<<_mm_extract_epi32(b, 1)<<" "<<_mm_extract_epi32(b, 2)<<" "<<_mm_extract_epi32(b, 3)<<"||";
    b = _mm256_extracti128_si256(item2, 1);
    cout << _mm_extract_epi32(b, 0)<<" "<<_mm_extract_epi32(b, 1)<<" "<<_mm_extract_epi32(b, 2)<<" "<<_mm_extract_epi32(b, 3)<<endl;

        ///////////////////////////////////////
    __m128i a1 = _mm256_extracti128_si256(binsContent, 0);
    cout << "bin1_xv4="<<_mm_extract_epi32(a1, 0)<<" "<<_mm_extract_epi32(a1, 1)<<" "<<_mm_extract_epi32(a1, 2)<<" "<<_mm_extract_epi32(a1, 3)<<"||";
    a1 = _mm256_extracti128_si256(binsContent, 1);
    cout << " "<<_mm_extract_epi32(a1, 0)<<" "<<_mm_extract_epi32(a1, 1)<<" "<<_mm_extract_epi32(a1, 2)<<" "<<_mm_extract_epi32(a1, 3)<<endl;

    ////////////////////////////////////



    __m256i match2 = _mm256_cmpeq_epi32(item2, binsContent);

            ///////////////////////////////////////
    a1 = _mm256_extracti128_si256(match2, 0);
    cout << "MATCHING="<<_mm_extract_epi32(a1, 0)<<" "<<_mm_extract_epi32(a1, 1)<<" "<<_mm_extract_epi32(a1, 2)<<" "<<_mm_extract_epi32(a1, 3)<<"||";
    a1 = _mm256_extracti128_si256(match2, 1);
    cout << " "<<_mm_extract_epi32(a1, 0)<<" "<<_mm_extract_epi32(a1, 1)<<" "<<_mm_extract_epi32(a1, 2)<<" "<<_mm_extract_epi32(a1, 3)<<endl;

    ////////////////////////////////////
    
    cout << "extract:" <<_mm256_movemask_epi8(match2) <<endl;
	  int mask2 = _mm256_movemask_epi8(match2) & 0xffff;
    cout << "mask:" <<mask2 <<endl;
    if (mask2 != 0) {
      int tz2 = _tzcnt_u32(mask2);
      cout << "tz mask:" <<tz2 << endl;
      cout << "tz extract:" <<_tzcnt_u32(_mm256_movemask_epi8(match2)) << endl;
      cout << "p:" <<p << endl;
      cout << "p1:" <<p1 << endl;
      int rowIndex = (tz2 < 3) ? p : p1;
      int counterNum = tz2 & 3;

      cout << "inccc= row:" << rowIndex << " counter:" << counterNum << " val:"<<value<<endl;
      if(incPool(rowIndex, counterNum,value)){


        num_item++;
        keys[rowIndex][counterNum]=key;
        table[rowIndex][counterNum]=fingerprint;
        table_bit[rowIndex][counterNum]=  (tz2 < 3) ? new_bit : ((1+new_bit)%2);
        return true;
      }
    }

    // there is not enough space in both bins or all counters are taken
    bool foundSpace = false;
    int t2 =0;
    while(!foundSpace){

      if(t2++ > 100){
        // thraw error massage
        victim_pointer=p;
        victim_fingerprint=fingerprint;
        return false; // insertion failed
      }

      //choose randomly one of the bins and choose rundomly a counter from it
      int j = rand() % 2;
      int counterNum = rand() % num_slots;
      p=p^(j*myhash(fingerprint,3,1<<30));
      p=p % cf_size;

      new_key = keys[p][counterNum];
      newf = table[p][counterNum];
      old_bit = table_bit[p][counterNum];
      val = delCounter(p,counterNum);

      // TODO: check if we can swap before deleting
      if(incPool(p,counterNum,value)){
        //printf("inserted %u in table[%d][%d] f=%u bit=%d\n",key,p,counterNum,fingerprint,j);
        //printf("moving %u with p=%d and bit %d\n",new_key,p,new_bit);
        
        keys[p][counterNum]=key;
        table[p][counterNum]=fingerprint;
        table_bit[p][counterNum]=(j +new_bit) %2;

        // find new home for cuckoo victim
        key = new_key;
        fingerprint = newf;
        value = val;
        new_bit=old_bit;

        foundSpace = true;
      }
      else{
        incPool(p,counterNum, val);
      }
    }



  }
  // thraw error massage
  victim_pointer=p;
  victim_fingerprint=fingerprint;
  return false; // insertion failed
}





template <typename key_type>
bool CF<key_type>::direct_insert(key_type key)
{
  if (cf_size==0) return true;
    if (query(key)) {
      return true;
    }
    int fingerprint=myhash(key,1,fp_size);
    int p=myhash(key,2,cf_size);
    p=p % cf_size;
    int jj=0;
    for (jj = 0;  jj < num_slots;  jj++) {
            //printf("di: item in table[%d][%d] for p=%d and f=%u\n",p,jj,p,fingerprint);
            if (table[p][jj] == -1){
                table[p][jj]=fingerprint;
                num_item++;
                //printf("inserted in table[%d][%d] f=%u\n",p,jj,fingerprint);
                return true;
            }
            int p1=p^myhash(fingerprint,3,1<<30);
            p1=p1 % cf_size;
            //printf("i2: item in table[%d][%d] for p1=%d and f=%u\n",p1,jj,p1,fingerprint);
            if (table[p1][jj] == -1) {
                table[p1][jj]=fingerprint;
                num_item++;
                //printf("inserted in table[%d][%d] f=%u\n",p1,jj,fingerprint);
                return true;
	    }
    } // all place are full
    int j = rand() % 2;
    jj = rand() % num_slots;
    p=p^(j*myhash(fingerprint,3,1<<30));
    p=p % cf_size;
    table[p][jj]=fingerprint;
    //printf("inserted in table[%d][%d] f=%u\n",p,jj,fingerprint);
    return true;
}







template <typename key_type>
bool CF<key_type>::direct_insert(const int p_in, const int f_in)
{
  //printf("----insert4---\n");
  if (cf_size==0) return true;
    int fingerprint=f_in; 
    int p=p_in % cf_size;
    int jj=0;
    for (jj = 0;  jj < num_slots;  jj++) {
            printf("di: item in table[%d][%d] for p=%d and f=%u\n",p,jj,p,fingerprint);
            if (table[p][jj] == -1){
                table[p][jj]=fingerprint;
                num_item++;
                printf("inserted in table[%d][%d] f=%u\n",p,jj,fingerprint);
                return true;
            }
            int p1=p^myhash(fingerprint,3,1<<30);
            p1=p1 % cf_size;
            printf("i2: item in table[%d][%d] for p1=%d and f=%u\n",p1,jj,p1,fingerprint);
            if (table[p1][jj] == -1) {
                table[p1][jj]=fingerprint;
                num_item++;
                printf("inserted in table[%d][%d] f=%u\n",p1,jj,fingerprint);
                return true;
	    }
    } // all place are full

    int j = rand() % 2;
    jj = rand() % num_slots;
    p=p^(j*myhash(fingerprint,3,1<<30));
    p=p % cf_size;
    table[p][jj]=fingerprint;
    printf("inserted in table[%d][%d] f=%u\n",p,jj,fingerprint);
    return true;
}

/*
 * Query
 */

template <typename key_type>
int CF<key_type>::query(const key_type key)
{
    int fingerprint=myhash(key,1,fp_size);
    fingerprint= fingerprint % fp_size;
    int p=myhash(key,2,cf_size);

    int p1=p^myhash(fingerprint,3,1<<30);
	  p1=p1 % cf_size;




    const __m256i item1 = _mm256_set1_epi32((int)fingerprint);
    __m128i bin1Content = *((__m128i*) table[p]);
    __m128i bin2Content = *((__m128i*) table[p1]);
    __m256i binsContent = _mm256_set_m128i(bin2Content, bin1Content);
    const __m256i match1 = _mm256_cmpeq_epi32(item1, binsContent);
	  const int mask1 = _mm256_movemask_epi8(match1) & 0xffff;
    if (mask1 != 0) {
      int tz1 = _tzcnt_u32(mask1);
      int rowIndex = (tz1 < 3) ? p : p1;
      int counterNum = tz1 & 3;
      int res = getVal(rowIndex,counterNum);
      return res;
    }
    return -1;



      

    


    /*
    if ((fingerprint==victim_fingerprint) && (p==victim_pointer)) {
            printf("query item %u in victim for p=%d and f=%d \n",key, p,fingerprint);
	    return true;
    }

    for (int j = 0;  j < 2;  j++) {
        p = myhash(key,2,cf_size)^(j*myhash(fingerprint,3,1<<30));
        p = p % cf_size;
        for (int jj = 0;  jj < num_slots;  jj++) {
            fingerprint= fingerprint % fp_size;
            //printf("query item %u in table[%d][%d] for p=%d and f=%d (0x%08x) with j=%d\n",key, p,jj,p,fingerprint,fingerprint,j);
            //printf("result is: %d (0x%08x),%d\n",table[p][jj],table[p][jj],table_bit[p][jj]);
            //printf("key is: %u\t",keys[p][jj]);
            //printf("p is %d  p2 is %d key f is %d \n",myhash(keys[p][jj],2,cf_size),myhash(keys[p][jj],2,cf_size)^myhash(table[p][jj],3,1<<30),myhash(keys[p][jj],1,fp_size));
            //printf("victim is p=%d and f=%d \n",victim_pointer,victim_fingerprint);
            num_access++;
            if ((table[p][jj] == fingerprint) && ((table_bit[p][jj]%2)==j)) {
                return true;
            }
        }
    }
    return false;*/
}




template <typename key_type>
std::pair<int,int> CF<key_type>::fullquery(const key_type key)
{
  if (cf_size==0) return make_pair(-1,-1);
    //std::cout << "<-->" << key.sip << "," << key.dip << "," << key.proto << "," << key.sp << "," << key.dp <<'\n';
    int fingerprint=myhash(key,1,fp_size);
    fingerprint= fingerprint % fp_size;
    int p=myhash(key,2,cf_size);
    if ((fingerprint==victim_fingerprint) && (p==victim_pointer)) return make_pair(-2,-2);
    for (int j = 0;  j < 2;  j++) {
        p = myhash(key,2,cf_size)^(j*myhash(fingerprint,3,1<<30));
        p = p % cf_size;
        for (int jj = 0;  jj < num_slots;  jj++) {
            fingerprint= fingerprint % fp_size;
            //printf("query item %u in table[%d][%d] for p=%d and f=%d with j=%d\n",key, p,jj,p,fingerprint,j);
            //printf("result is: %d,%d\n",table[p][jj],table_bit[p][jj]);
            num_access++;
            if ((table[p][jj] == fingerprint) && ((table_bit[p][jj]%2)==j)) {
                return make_pair(p,jj);
            }
        }
    }
    return make_pair(-1,-1);
}

template <typename key_type>
std::pair<int,int> CF<key_type>::get_pf(const key_type key) {
    int fingerprint=myhash(key,1,fp_size);
    fingerprint= fingerprint % fp_size;
    int p=myhash(key,2,cf_size);
    return make_pair(p,fingerprint);
}

//template class CF<five_tuple>;
template class CF<int>;
