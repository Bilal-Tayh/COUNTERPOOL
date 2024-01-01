#ifndef CF_s
#define CF_s

#include <utility>
#include <cstdint> // include this header for uint64_t
#include <unordered_map>
#include "../../CounterPoolsDefs.h"


using namespace std;


#define _mm256_set_m128i(v0, v1)  _mm256_insertf128_si256(_mm256_castsi128_si256(v1), (v0), 1)

#define _mm256_setr_m128i(v0, v1) _mm256_set_m128i((v1), (v0))



// https://stackoverflow.com/questions/8752837/undefined-reference-to-template-class-constructor
// add in the CF.cpp the template class eg:


template <typename key_type> class CF {
		//int ***table;//  memory
		int **keys;//  memory
		int **table;//  memory
		int **table_bit;//  memory
		int   cf_size; // size of CF memory
		int   fp_size;    // 1<<f
		int   num_item;   	// number of inserted item
		int   num_access;   	// number of inserted item
		int   num_slots;   	// number of slots
		int victim_fingerprint;
		int victim_pointer;
		int hash_type;
		bool insert2(key_type key,int p,int fingerprint);


        uint64_t* m_pools;
        uint16_t* m_encodings;

        bool m_initLookupTable;
        uint32_t m_lookup[STARS_AND_BARS_64_4];

        void initLookupTableFunc();

        uint32_t decode_sizes(uint16_t encoding, uint64_t n, uint64_t k);
        uint32_t decode_offsets(uint16_t encoding, uint64_t n, uint64_t k);

        uint16_t encode(uint32_t sizes);
        uint16_t encode_without_auxilary_map(uint32_t sizes);

        std::unordered_map< uint64_t, uint16_t> m_auxilary_map;

		public:
		CF(int M,int f, int slot, int hash_type_param);
		//CF(int M,int f);
		virtual ~CF();
		void clear();
		void dump();

		bool direct_insert(const key_type key);
		//bool direct_insert(const int p, const int f);
		bool direct_insert(const int p, const int f);
		bool insert(const key_type key);
		int query(const key_type key);
		std::pair<int,int> fullquery(const key_type key);
		bool cache_query(const key_type key);
		bool check(const key_type key) {return query(key);}
		pair<int,int> get_pf(const key_type key);
		int get_nslots() {return num_slots;}
		int get_nitem() {return num_item;}
		int get_size() {return  num_slots*cf_size;}
		int get_numaccess() {return num_access;}

		private:
		void incPoolCounter(int index, int counterNum, int value, int bitDiff);
		bool incPool(int index, int counterNum , uint64_t value);
		uint64_t delCounter(int index, int counterNum);
		uint64_t getVal(int index, int counterNum);
		int myhash(key_type key, int i, int s);
};

#endif 
