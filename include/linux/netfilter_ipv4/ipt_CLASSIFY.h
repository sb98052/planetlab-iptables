#ifndef _IPT_CLASSIFY_H
#define _IPT_CLASSIFY_H

struct ipt_classify_target_info {
	u_int32_t priority;
	u_int8_t add_mark;
};

#endif /*_IPT_CLASSIFY_H */
