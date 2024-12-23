def all_flags():
    '''
    All Intel and AMD flags defined in https://github.com/torvalds/linux/blob/master/arch/x86/include/asm/cpufeatures.h, 

    except for the following:
    1. ARM CPU features
    2. Other manufacturer CPU features
    3. Thermal and Power Management
    4. Bug-related words
    '''
    # Intel
    CPUID_1_EDX = ['fpu', 'vme', 'de', 'pse', 'tsc', 'msr', 'pae', 'mce', 'cx8', 'apic', 'sep', 'mtrr', 'pge', 'mca', 'cmov', 'pat', 'pse36', 'pn', 'clflush', 'dts', 'acpi', 'mmx', 'fxsr', 'sse', 'sse2', 'ss', 'ht', 'tm', 'ia64', 'pbe']
    CPUID_1_ECX = ['pni', 'pclmulqdq', 'dtes64', 'monitor', 'ds_cpl', 'vmx', 'smx', 'est', 'tm2', 'ssse3', 'cid', 'sdbg', 'fma', 'cx16', 'xtpr', 'pdcm', 'pcid', 'dca', 'sse4_1', 'sse4_2', 'x2apic', 'movbe', 'popcnt', 'tsc_deadline_timer', 'aes', 'xsave', 'osxsave', 'avx', 'f16c', 'rdrand', 'hypervisor']
    CPUID_7_0_EBX = ['fsgsbase', 'tsc_adjust', 'sgx', 'bmi1', 'hle', 'avx2', 'fdp_excptn_only', 'smep', 'bmi2', 'erms', 'invpcid', 'rtm', 'cqm', 'zero_fcs_fds', 'mpx', 'rdt_a', 'avx512f', 'avx512dq', 'rdseed', 'adx', 'smap', 'avx512ifma', 'clflushopt', 'clwb', 'intel_pt', 'avx512pf', 'avx512er', 'avx512cd', 'sha_ni', 'avx512bw', 'avx512vl']
    CPUID_7_1_EAX = ['avx_vnni', 'avx512_bf16', 'cmpccxadd', 'arch_perfmon_ext', 'fzrm', 'fsrs', 'fsrc', 'lkgs', 'amx_fp16', 'avx_ifma']
    CPUID_7_0_ECX = ['avx512vbmi', 'umip', 'pku', 'ospke', 'waitpkg', 'avx512_vbmi2', 'gfni', 'vaes', 'vpclmulqdq', 'avx512_vnni', 'avx512_bitalg', 'tme', 'avx512_vpopcntdq', 'la57', 'rdpid', 'bus_lock_detect', 'cldemote', 'movdiri', 'movdir64b', 'enqcmd', 'sgx_lc']
    CPUID_7_0_EDX = ['avx512_4vnniw', 'avx512_4fmaps', 'fsrm', 'avx512_vp2intersect', 'srbds_ctrl', 'md_clear', 'rtm_always_abort', 'tsx_force_abort', 'serialize', 'hybrid_cpu', 'tsxldtrk', 'pconfig', 'arch_lbr', 'ibt', 'amx_bf16', 'avx512_fp16', 'amx_tile', 'amx_int8', 'spec_ctrl', 'intel_stibp', 'flush_l1d', 'arch_capabilities', 'core_capabilities', 'spec_ctrl_ssbd']

    # AMD
    CPUID_8000_0001_EDX = ['syscall', 'mp', 'nx', 'mmxext', 'fxsr_opt', 'pdpe1gb', 'rdtscp', 'lm', '3dnowext', '3dnow']
    CPUID_8000_0001_ECX = ['lahf_lm', 'cmp_legacy', 'svm', 'extapic', 'cr8_legacy', 'abm', 'sse4a', 'misalignsse', '3dnowprefetch', 'osvm', 'ibs', 'xop', 'skinit', 'wdt', 'lwp', 'fma4', 'tce', 'nodeid_msr', 'tbm', 'topoext', 'perfctr_core', 'perfctr_nb', 'bpext', 'ptsc', 'perfctr_llc', 'mwaitx']
    CPUID_8000_0008_EBX = ['clzero', 'irperf', 'xsaveerptr', 'rdpru', 'wbnoinvd', 'amd_ibpb', 'amd_ibrs', 'amd_stibp', 'amd_stibp_always_on', 'amd_ppin', 'amd_ssbd', 'virt_ssbd', 'amd_ssb_no', 'cppc', 'btc_no', 'brs']
    # CPUID_8000_000a_EDX : AMD SVM(Secure Virtual Machine) features, 하드웨어 기반 가상화를 지원하는 기술
    CPUID_8000_000a_EDX = ['npt', 'lbrv', 'svm_lock', 'nrip_save','tsc_scale', 'vmcb_clean', 'flushbyasid', 'decodeassists', 'pausefilter', 'pfthreshold', 'avic', 'v_vmsave_vmload', 'vgif', 'x2avic', 'v_spec_ctrl', 'svme_addr_chk']
    CPUID_8000_0007_EBX = ['overflow_recov', 'succor', 'smca']
    # CPUID_8000_001f_EAX : AMD-defined memory encryption features
    CPUID_8000_001f_EAX = ['sme', 'sev', 'vm_page_flush', 'sev_es', 'v_tsc_aux', 'sme_coherent']
    # CPUID_8000_0021_EAX : AMD-defined Extended Feature 2 EAX
    CPUID_8000_0021_EAX = ['no_nested_data_bp', 'lfence_rdtsc', 'null_sel_clr_base', 'autoibrs', 'no_smm_ctl_msr']

    # Linux
    CPUID_LNX_Other = ['cxmmx', 'k6_mtrr', 'cyrix_arr', 'centaur_mcr', 'k8', 'p3', 'p4', 'constant_tsc', 'up', 'art', 'arch_perfmon', 'pebs', 'bts', 'syscall32', 'sysenter32', 'rep_good', 'amd_lbr_v2', 'acc_power', 'nopl', 'always', 'xtopology', 'tsc_reliable', 'nonstop_tsc', 'cpuid', 'amd_dcm', 'aperfmperf', 'rapl', 'nonstop_tsc_s3', 'tsc_known_freq']
    CPUID_LNX_Auxiliary = ['ring3mwait', 'cpuid_fault', 'cpb', 'epb', 'cat_l3', 'cat_l2', 'cdp_l3', 'invpcid_single', 'hw_pstate', 'proc_feedback', 'xcompacted', 'pti', 'kernel_ibrs', 'rsb_vmexit', 'intel_ppin', 'cdp_l2', 'msr_spec_ctrl', 'ssbd', 'mba', 'rsb_ctxsw', 'perfmon_v2', 'use_ibpb', 'use_ibrs_fw', 'spec_store_bypass_disable', 'ls_cfg_ssbd', 'ibrs', 'ibpb', 'stibp', 'zen', 'l1tf_pteinv', 'ibrs_enhanced', 'msr_ia32_feat_ctl']
    CPUID_LNX_Virtualization = ['tpr_shadow', 'vnmi', 'flexpriority', 'ept', 'vpid', 'vmmcall', 'xenpv', 'ept_ad', 'vmcall', 'vmw_vmmcall', 'pvunlock', 'vcpupreempt', 'tdx_guest']
    CPUID_LNX_Extended_Auxiliary = ['cqm_llc', 'cqm_occup_llc', 'cqm_mbm_total', 'cqn_mbm_local', 'fence_swapgs_user', 'fence_swapgs_kernel', 'split_lock_detect', 'per_thread_mba', 'sgx1', 'sgx2', 'entry_ibpb', 'rrsba_ctrl', 'retpoline', 'retpoline_lfence', 'rethunk', 'unret', 'use_ibpb_fw', 'rsb_vmexit_lite', 'sgx_edeccssa', 'call_depth', 'msr_tsx_ctrl', 'smba', 'bmec']

    # Extended state features
    CPUID_D_1_EAX = ['xsaveopt', 'xsavec', 'xgetbv1', 'xsaves', 'xfd']

    # All
    CPU_FEATURES = CPUID_1_EDX + CPUID_1_ECX + CPUID_7_0_EBX + CPUID_7_1_EAX + CPUID_7_0_ECX + CPUID_7_0_EDX + CPUID_8000_0001_EDX + CPUID_8000_0001_ECX + CPUID_8000_0008_EBX + CPUID_8000_000a_EDX + CPUID_8000_0007_EBX + CPUID_8000_001f_EAX + CPUID_8000_0021_EAX + CPUID_LNX_Other + CPUID_LNX_Auxiliary + CPUID_LNX_Virtualization + CPUID_LNX_Extended_Auxiliary + CPUID_D_1_EAX
    
    return CPU_FEATURES

def all_CPU_features_simplification_by_lscpu():
    '''
    "lscpu_all_vendors.csv" 에서 현재 지원되지 않는 인스턴스를 제외하고 AWS, GCP, Azure 모든 인스턴스에 존재하거나 존재하지 않는 flags 제거
    '''
    # Intel
    CPUID_1_EDX = ['ss']
    CPUID_1_ECX = ['monitor', 'vmx', 'est', 'pcid', 'x2apic', 'tsc_deadline_timer']
    CPUID_7_0_EBX = ['tsc_adjust', 'hle', 'erms', 'invpcid', 'rtm', 'mpx', 'avx512f', 'avx512dq', 'rdseed', 'adx', 'smap', 'avx512ifma', 'clflushopt', 'clwb', 'avx512cd', 'sha_ni', 'avx512bw', 'avx512vl']
    CPUID_7_0_ECX = ['avx512vbmi', 'umip', 'pku', 'ospke', 'avx512_vbmi2', 'gfni', 'vaes', 'vpclmulqdq', 'avx512_vnni', 'avx512_bitalg', 'tme', 'avx512_vpopcntdq', 'rdpid']
    CPUID_7_0_EDX = ['md_clear', 'flush_l1d', 'arch_capabilities', ]

    # AMD
    CPUID_8000_0001_EDX = ['mmxext', 'fxsr_opt', 'pdpe1gb']
    CPUID_8000_0001_ECX = ['cmp_legacy', 'svm', 'cr8_legacy', 'sse4a', 'misalignsse', '3dnowprefetch', 'topoext', 'perfctr_core']
    CPUID_8000_0008_EBX = ['clzero', 'xsaveerptr', 'rdpru', 'wbnoinvd']
    # CPUID_8000_000a_EDX : AMD SVM(Secure Virtual Machine) features, 하드웨어 기반 가상화를 지원하는 기술
    CPUID_8000_000a_EDX = ['npt', 'nrip_save','tsc_scale', 'vmcb_clean', 'flushbyasid', 'decodeassists', 'pausefilter', 'pfthreshold', 'v_vmsave_vmload']

    # Linux
    CPUID_LNX_Other = ['constant_tsc', 'arch_perfmon', 'xtopology', 'tsc_reliable', 'nonstop_tsc', 'amd_dcm', 'aperfmperf', 'tsc_known_freq']
    CPUID_LNX_Auxiliary = ['cpuid_fault', 'invpcid_single', 'pti', 'ssbd', 'ibrs', 'ibpb', 'stibp', 'ibrs_enhanced', ]
    CPUID_LNX_Virtualization = ['tpr_shadow', 'vnmi', 'ept', 'vpid', 'vmmcall', 'ept_ad']

    # Extended state features
    CPUID_D_1_EAX = ['xsavec', 'xgetbv1', 'xsaves']

    # All
    CPU_FEATURES = CPUID_1_EDX + CPUID_1_ECX + CPUID_7_0_EBX + CPUID_7_0_ECX + CPUID_7_0_EDX + CPUID_8000_0001_EDX + CPUID_8000_0001_ECX + CPUID_8000_0008_EBX + CPUID_8000_000a_EDX + CPUID_LNX_Other + CPUID_LNX_Auxiliary + CPUID_LNX_Virtualization + CPUID_D_1_EAX
    
    return CPU_FEATURES