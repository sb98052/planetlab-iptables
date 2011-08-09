# $Id$
# $URL$
#
WEBFETCH		:= wget
SHA1SUM			:= sha1sum

ALL			+= iptables ipset
iptables-URL		:= http://www.netfilter.org/projects/iptables/files/iptables-1.4.10.tar.bz2
iptables-SHA1SUM	:= 8190b8c9714a3eec825317e8ac1deeb3d11c6d29
ipset-URL		:= http://ipset.netfilter.org/ipset-4.5.tar.bz2
ipset-SHA1SUM	:= 696a5cd96459c8fb028f0dfb9927a5c4f183d28b
iptables		:= $(notdir $(iptables-URL))
ipset		:= $(notdir $(ipset-URL))

all: $(ALL)
.PHONY: all

##############################
define download_target
$(1): $($(1))
.PHONY: $($(1))
$($(1)): 
	@if [ ! -e "$($(1))" ] ; then echo "$(WEBFETCH) $($(1)-URL)" ; $(WEBFETCH) $($(1)-URL) ; fi
	@if [ ! -e "$($(1))" ] ; then echo "Could not download source file: $($(1)) does not exist" ; exit 1 ; fi
	@if test "$$$$($(SHA1SUM) $($(1)) | awk '{print $$$$1}')" != "$($(1)-SHA1SUM)" ; then \
	    echo "sha1sum of the downloaded $($(1)) does not match the one from 'Makefile'" ; \
	    echo "Local copy: $$$$($(SHA1SUM) $($(1)))" ; \
	    echo "In Makefile: $($(1)-SHA1SUM)" ; \
	    false ; \
	else \
	    ls -l $($(1)) ; \
	fi
endef

$(eval $(call download_target,iptables))

sources: $(ALL) 
.PHONY: sources

####################
# default - overridden by the build
SPECFILE = iptables.spec

PWD=$(shell pwd)
PREPARCH ?= noarch
RPMDIRDEFS = --define "_sourcedir $(PWD)" --define "_builddir $(PWD)" --define "_srcrpmdir $(PWD)" --define "_rpmdir $(PWD)"
trees: sources
	rpmbuild $(RPMDIRDEFS) $(RPMDEFS) --nodeps -bp --target $(PREPARCH) $(SPECFILE)

srpm: sources
	rpmbuild $(RPMDIRDEFS) $(RPMDEFS) --nodeps -bs $(SPECFILE)

TARGET ?= $(shell uname -m)
rpm: sources
	rpmbuild $(RPMDIRDEFS) $(RPMDEFS) --nodeps --target $(TARGET) -bb $(SPECFILE)

clean:
	rm -f *.rpm *.tgz *.bz2 *.gz

++%: varname=$(subst +,,$@)
++%:
	@echo "$(varname)=$($(varname))"
+%: varname=$(subst +,,$@)
+%:
	@echo "$($(varname))"
