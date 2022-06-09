#include <iostream>
#include <memory>
#include <thread>
#include <algorithm>
#include <deque>
#include <regex>
#include <chrono>
#include "gtest/gtest.h"
#include "events_common.h"
#include "events.h"
#include "../src/eventd.h"

using namespace std;

#define ARRAY_SIZE(p) ((int)(sizeof(p) / sizeof((p)[0])))

typedef struct {
    int id;
    string source;
    string tag;
    string rid;
    string seq;
    event_params_t params;
    int missed_cnt;
} test_data_t;

internal_event_t create_ev(const test_data_t &data)
{
    internal_event_t event_data;

    {
        string param_str;

        EXPECT_EQ(0, serialize(data.params, param_str));

        map_str_str_t event_str_map = { { data.source + ":" + data.tag, param_str}};

        EXPECT_EQ(0, serialize(event_str_map, event_data[EVENT_STR_DATA]));
    }

    event_data[EVENT_RUNTIME_ID] = data.rid;
    event_data[EVENT_SEQUENCE] = data.seq;

    return event_data;
}

/* Mock test data with event parameters and expected missed count */
static const test_data_t ldata[] = {
    {
        0,
        "source0",
        "tag0",
        "guid-0",
        "1",
        {{"ip", "10.10.10.10"}, {"state", "up"}},
        0
    },
    {
        1,
        "source0",
        "tag1",
        "guid-1",
        "100",
        {{"ip", "10.10.27.10"}, {"state", "down"}},
        0
    },
    {
        2,
        "source1",
        "tag2",
        "guid-2",
        "101",
        {{"ip", "10.10.24.10"}, {"state", "down"}},
        0
    },
    {
        3,
        "source0",
        "tag3",
        "guid-1",
        "105",
        {{"ip", "10.10.10.10"}, {"state", "up"}},
        4
    },
    {
        4,
        "source0",
        "tag4",
        "guid-0",
        "2",
        {{"ip", "10.10.20.10"}, {"state", "down"}},
        0
    },
    {
        5,
        "source1",
        "tag5",
        "guid-2",
        "110",
        {{"ip", "10.10.24.10"}, {"state", "down"}},
        8
    },
    {
        6,
        "source0",
        "tag0",
        "guid-0",
        "5",
        {{"ip", "10.10.10.10"}, {"state", "up"}},
        2
    },
    {
        7,
        "source0",
        "tag1",
        "guid-1",
        "106",
        {{"ip", "10.10.27.10"}, {"state", "down"}},
        0
    },
    {
        8,
        "source1",
        "tag2",
        "guid-2",
        "111",
        {{"ip", "10.10.24.10"}, {"state", "down"}},
        0
    },
    {
        9,
        "source0",
        "tag3",
        "guid-1",
        "109",
        {{"ip", "10.10.10.10"}, {"state", "up"}},
        2
    },
    {
        10,
        "source0",
        "tag4",
        "guid-0",
        "6",
        {{"ip", "10.10.20.10"}, {"state", "down"}},
        0
    },
    {
        11,
        "source1",
        "tag5",
        "guid-2",
        "119",
        {{"ip", "10.10.24.10"}, {"state", "down"}},
        7
    },
};


void run_cap(void *zctx, bool &term, string &read_source,
        int &cnt)
{
    void *mock_cap = zmq_socket (zctx, ZMQ_SUB);
    string source;
    internal_event_t ev_int;
    int block_ms = 200;
    int i=0;

    EXPECT_TRUE(NULL != mock_cap);
    EXPECT_EQ(0, zmq_connect(mock_cap, get_config(CAPTURE_END_KEY).c_str()));
    EXPECT_EQ(0, zmq_setsockopt(mock_cap, ZMQ_SUBSCRIBE, "", 0));
    EXPECT_EQ(0, zmq_setsockopt(mock_cap, ZMQ_RCVTIMEO, &block_ms, sizeof (block_ms)));

    while(!term) {
        zmq_msg_t source, data;
        zmq_msg_init(&source);
        zmq_msg_init(&data);
        int rc = zmq_msg_recv(&source, mock_cap, 0);
        if (rc != -1) {
            rc = zmq_msg_recv(&data, mock_cap, 0);
        }
        if (rc != -1) {
            cnt = ++i;
        }
        else {
            printf("CAP failed rc=%d zerrno=%d\n", rc, zerrno);
        }
    }

    zmq_close(mock_cap);
    printf("run_cap exited =%d\n", cnt);
}

void run_sub(void *zctx, bool &term, string &read_source, internal_events_lst_t &lst,
        int &cnt)
{
    void *mock_sub = zmq_socket (zctx, ZMQ_SUB);
    string source;
    internal_event_t ev_int;
    int block_ms = 200;

    EXPECT_TRUE(NULL != mock_sub);
    EXPECT_EQ(0, zmq_connect(mock_sub, get_config(XPUB_END_KEY).c_str()));
    EXPECT_EQ(0, zmq_setsockopt(mock_sub, ZMQ_SUBSCRIBE, "", 0));
    EXPECT_EQ(0, zmq_setsockopt(mock_sub, ZMQ_RCVTIMEO, &block_ms, sizeof (block_ms)));

    while(!term) {
        if (0 == zmq_message_read(mock_sub, 0, source, ev_int)) {
            lst.push_back(ev_int);
            read_source.swap(source);
            cnt = (int)lst.size();
        }
    }

    zmq_close(mock_sub);
    printf("run_sub exited =%d\n", (int)lst.size());
}

void *init_pub(void *zctx)
{
    void *mock_pub = zmq_socket (zctx, ZMQ_PUB);
    EXPECT_TRUE(NULL != mock_pub);
    EXPECT_EQ(0, zmq_connect(mock_pub, get_config(XSUB_END_KEY).c_str()));

    return mock_pub;
}

void run_pub(void *mock_pub, const string wr_source, internal_events_lst_t &lst)
{
    for(internal_events_lst_t::const_iterator itc = lst.begin(); itc != lst.end(); ++itc) {
        EXPECT_EQ(0, zmq_message_send(mock_pub, wr_source, *itc));
    }
    printf("Published %d events\n", (int)lst.size());
}


TEST(eventd, proxy)
{
    printf("PROxy TEST started\n");
    {
        /* Direct log messages to stdout */
        string dummy, op("STDOUT");
        swss::Logger::swssOutputNotify(dummy, op);
    }
    bool term_sub = false;
    bool term_cap = false;
    string rd_csource, rd_source, wr_source("hello");
    internal_events_lst_t rd_evts, wr_evts;
    int rd_evts_sz = 0, rd_cevts_sz = 0;
    int wr_sz;

    void *zctx = zmq_ctx_new();
    EXPECT_TRUE(NULL != zctx);

    eventd_proxy *pxy = new eventd_proxy(zctx);
    EXPECT_TRUE(NULL != pxy);

    /* Starting proxy */
    EXPECT_EQ(0, pxy->init());

    /* subscriber in a thread */
    thread thr(&run_sub, zctx, ref(term_sub), ref(rd_source), ref(rd_evts), ref(rd_evts_sz));

    /* capture in a thread */
    thread thrc(&run_cap, zctx, ref(term_cap), ref(rd_csource), ref(rd_cevts_sz));

    /* Init pub connection */
    void *mock_pub = init_pub(zctx);

    /* Provide time for async connect to complete */
    this_thread::sleep_for(chrono::milliseconds(100));

    EXPECT_TRUE(5 < ARRAY_SIZE(ldata));

    for(int i=0; i<5; ++i) {
        wr_evts.push_back(create_ev(ldata[i]));
    }

    EXPECT_TRUE(rd_evts.empty());
    EXPECT_TRUE(rd_source.empty());

    /* Publish events. */
    run_pub(mock_pub, wr_source, wr_evts);

    wr_sz = (int)wr_evts.size();
    for(int i=0; (wr_sz != rd_evts_sz) && (i < 100); ++i) {
        /* Loop & wait for atmost a second */
        printf("rd_evts.size != wr_evts.size %d != %d\n", 
                (int)rd_evts.size(), (int)wr_evts.size());
        this_thread::sleep_for(chrono::milliseconds(10));
    }
    this_thread::sleep_for(chrono::milliseconds(1000));

    delete pxy;
    pxy = NULL;

    term_sub = true;
    term_cap = true;

    thr.join();
    thrc.join();
    printf("wr=%d rd=%d rdc=%d\n", (int)wr_evts.size(), (int)rd_evts.size(),
            rd_cevts_sz);
    EXPECT_EQ(rd_evts.size(), wr_evts.size());
    EXPECT_EQ(rd_cevts_sz,  wr_evts.size());

    zmq_close(mock_pub);
    zmq_ctx_term(zctx);
    printf("eventd_proxy is tested GOOD\n");
}


#if 0
TEST(eventd, capture)
{
    printf("Capture TEST started\n");
    {
        /* Direct log messages to stdout */
        string dummy, op("STDOUT");
        swss::Logger::swssOutputNotify(dummy, op);
        swss::Logger::setMinPrio(swss::Logger::SWSS_DEBUG);
    }

    string wr_source("hello");
    internal_events_lst_t wr_evts;
    int init_cache = 3;
    int cache_max = init_cache + 3;
    event_serialized_lst_t evts_start, evts_expect, evts_read;
    last_events_t last_evts_exp, last_evts_read;

    void *zctx = zmq_ctx_new();
    EXPECT_TRUE(NULL != zctx);

    /* Run the proxy; Capture service reads from proxy */
    eventd_proxy *pxy = new eventd_proxy(zctx);
    EXPECT_TRUE(NULL != pxy);

    /* Starting proxy */
    EXPECT_EQ(0, pxy->init());

    /* Create capture service */
    capture_service *pcap = new capture_service(zctx, cache_max);

    /* Expect START_CAPTURE */
    EXPECT_EQ(-1, pcap->set_control(STOP_CAPTURE));

    EXPECT_TRUE(init_cache > 1);
    EXPECT_TRUE((cache_max+3) < ARRAY_SIZE(ldata));

    /* Collect few serailized strings of events for startup cache */
    for(int i=0; i < init_cache; ++i) {
        internal_event_t ev(create_ev(ldata[i]));
        string evt_str;
        serialize(ev, evt_str);
        evts_start.push_back(evt_str);
        evts_expect.push_back(evt_str);
    }

    /*
     * Collect events to publish for capture to cache
     * re-publishing some events sent in cache.
     */
    for(int i=1; i < ARRAY_SIZE(ldata); ++i) {
        internal_event_t ev(create_ev(ldata[i]));
        string evt_str;

        serialize(ev, evt_str);

        wr_evts.push_back(ev);

        if (i < cache_max) {
            if (i >= init_cache)
                evts_expect.push_back(evt_str);
        } else {
            /* collect last entries for overflow */
            last_evts_exp[ldata[i].rid] = evt_str;
        }
    }

    EXPECT_EQ(0, pcap->set_control(INIT_CAPTURE));
    EXPECT_EQ(0, pcap->set_control(START_CAPTURE, &evts_start));

    /* Init pub connection */
    void *mock_pub = init_pub(zctx);

    /* Provide time for async connect to complete */
    this_thread::sleep_for(chrono::milliseconds(4000));

    /* Publish events from 1 to all. */
    run_pub(mock_pub, wr_source, wr_evts);

    /* Provide time for async message receive. */
    this_thread::sleep_for(chrono::milliseconds(4000));

    /* Stop capture, closes socket & terminates the thread */
    EXPECT_EQ(0, pcap->set_control(STOP_CAPTURE));

    /* Read the cache */
    EXPECT_EQ(0, pcap->read_cache(evts_read, last_evts_read));

    printf("evts_read=%d evts_expect=%d\n", (int)evts_read.size(), (int)evts_expect.size());
    EXPECT_EQ(evts_read, evts_expect);
    EXPECT_EQ(last_evts_read, last_evts_exp);

    delete pxy;
    pxy = NULL;

    delete pcap;
    pcap = NULL;

    zmq_close(mock_pub);
    zmq_ctx_term(zctx);
    printf("eventd_proxy is tested GOOD\n");
}
#endif

