IPSET_VERSION:=2.3.0

IPSET_LIB_DIR:=$(LIBDIR)/ipset

IPSET_CFLAGS:=# -g -DIPSET_DEBUG #-pg # -DIPTC_DEBUG
SETTYPES:=ipmap portmap macipmap iphash nethash iptree iptreemap ipporthash

# for building on fedora 8
ifneq "$(shell ld --help | grep build-id)" ""
#not needed# CFLAGS += -Wl,--build-id
LD += --build-id
endif

ifneq ($(wildcard $(KERNEL_DIR)/include/linux/netfilter_ipv4/ip_set.h),)

EXTRAS+=ipset/ipset
EXTRAS+=$(foreach T, $(SETTYPES),ipset/libipset_$(T).so)
EXTRA_INSTALLS+=$(DESTDIR)$(BINDIR)/ipset $(DESTDIR)$(MANDIR)/man8/ipset.8
EXTRA_INSTALLS+=$(foreach T, $(SETTYPES), $(DESTDIR)$(LIBDIR)/ipset/libipset_$(T).so)

#Dependencies
ipset/libipset.d: $(foreach T, $(SETTYPES),ipset/ipset_$(T).c)
	@-$(CC) -M -MG $(CFLAGS) $(IPSET_CFLAGS) $^ | sed -e 's@^.*\.o:@$*.d $*.a($*.o):@' > $@

#The ipset(8) self
ipset/ipset.o: ipset/ipset.c
	$(CC) $(CFLAGS) $(IPSET_CFLAGS) -DIPSET_VERSION=\"$(IPSET_VERSION)\" -DIPSET_LIB_DIR=\"$(IPSET_LIB_DIR)\" -c -o $@ $<

ipset/ipset: ipset/ipset.o
	$(CC) $(CFLAGS) $(IPSET_CFLAGS) -ldl -rdynamic -o $@ $^

#Pooltypes
ipset/ipset_%.o: ipset/ipset_%.c
	$(CC) $(SH_CFLAGS) $(IPSET_CFLAGS) -o $@ -c $<

ipset/libipset_%.so: ipset/ipset_%.o
	$(CC) -shared -o $@ $<

$(DESTDIR)$(LIBDIR)/ipset/libipset_%.so: ipset/libipset_%.so
	@[ -d $(DESTDIR)$(LIBDIR)/ipset ] || mkdir -p $(DESTDIR)$(LIBDIR)/ipset
	cp $< $@

$(DESTDIR)$(BINDIR)/ipset: ipset/ipset
	@[ -d $(DESTDIR)$(BINDIR) ] || mkdir -p $(DESTDIR)$(BINDIR)
	cp $< $@

$(DESTDIR)$(MANDIR)/man8/ipset.8: ipset/ipset.8
	@[ -d $(DESTDIR)$(MANDIR)/man8 ] || mkdir -p $(DESTDIR)$(MANDIR)/man8
	cp $< $@

endif
