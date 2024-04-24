#ifndef CP_TESTS
#define CP_TESTS

///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////

// cms
void test_cms_error_on_arrival_sanity_64_4_0_1(int N, int width, int height, int seed, const char* data);
void test_cms_error_on_arrival_64_4_0_1(int N, int width, int height, int seed, const char* data);
void test_cms_speed_64_4_0_1(int N, int width, int height, int seed, const char* data);

///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////

// cms
void test_cms_error_on_arrival_pools(int N, int width, int height, int seed, const char* data, int pool_bit_size, int counters_per_pool, int initial_counter_size, int counter_bit_increase, int k);
void test_cms_error_on_arrival_pools_HH(int N, int width, int height, int seed, const char* data, int pool_bit_size, int counters_per_pool, int initial_counter_size, int counter_bit_increase, int k);
void test_cms_error_on_arrival_pools_cus_HH(int N, int width, int height, int seed, const char* data, int pool_bit_size, int counters_per_pool, int initial_counter_size, int counter_bit_increase, int k);
void test_cms_error_on_arrival_pools_etk(int N, int width, int height, int seed, const char* data, int pool_bit_size, int counters_per_pool, int initial_counter_size, int counter_bit_increase, int k);
void test_cms_error_on_arrival_pools_HH_cuckoo(int N, int width, int height, int seed, const char* data, int pool_bit_size, int counters_per_pool, int initial_counter_size, int counter_bit_increase, int k);
void test_cms_error_on_arrival_pools_HH_NoFail1(int N, int width, int height, int seed, const char* data, int pool_bit_size, int counters_per_pool, int initial_counter_size, int counter_bit_increase, int k);
void test_cms_error_on_arrival_pools_HH_NoFail2(int N, int width, int height, int seed, const char* data, int pool_bit_size, int counters_per_pool, int initial_counter_size, int counter_bit_increase, int k);
void test_cms_error_on_arrival_pools_HH_NoFail3(int N, int width, int height, int seed, const char* data, int pool_bit_size, int counters_per_pool, int initial_counter_size, int counter_bit_increase, int k);

///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////

// sim sanity
void sim_test_cms_error_on_arrival_sanity(int N, int width, int height, int seed, const char* data);

///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////

// sim sanity
void test_cms_error_on_arrival_pools_sanity(int N, int width, int height, int seed, const char* data, int pool_bit_size, int counters_per_pool, int initial_counter_size, int counter_bit_increase, int k);

///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////

// top k sanity
void test_cms_error_on_arrival_top_k_sanity(int N, int width, int height, int seed, const char* data, int pool_bit_size, int counters_per_pool, int initial_counter_size, int counter_bit_increase, int k);

///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////

// read/write files
void test_cms_rw_files_pools(int N, int width, int height, int seed, const char* data, int pool_bit_size, int counters_per_pool, int initial_counter_size, int counter_bit_increase, int k);

#endif
