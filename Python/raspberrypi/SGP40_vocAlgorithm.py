
VocAlgorithm_SAMPLING_INTERVAL                           = (1.)
VocAlgorithm_INITIAL_BLACKOUT                            = (45.)
VocAlgorithm_VOC_INDEX_GAIN                              = (230.)
VocAlgorithm_SRAW_STD_INITIAL                            = (50.)
VocAlgorithm_SRAW_STD_BONUS                              = (220.)
VocAlgorithm_TAU_MEAN_VARIANCE_HOURS                     = (12.)
VocAlgorithm_TAU_INITIAL_MEAN                            = (20.)
VocAlgorithm_INIT_DURATION_MEAN                          = (3600. * 0.75)
VocAlgorithm_INIT_TRANSITION_MEAN                        = (0.01)
VocAlgorithm_TAU_INITIAL_VARIANCE                        = (2500.)
VocAlgorithm_INIT_DURATION_VARIANCE                      = ((3600. * 1.45))
VocAlgorithm_INIT_TRANSITION_VARIANCE                    = (0.01)
VocAlgorithm_GATING_THRESHOLD                            = (340.)
VocAlgorithm_GATING_THRESHOLD_INITIAL                    = (510.)
VocAlgorithm_GATING_THRESHOLD_TRANSITION                 = (0.09)
VocAlgorithm_GATING_MAX_DURATION_MINUTES                 = ((60. * 3.))
VocAlgorithm_GATING_MAX_RATIO                            = (0.3)
VocAlgorithm_SIGMOID_L                                   = (500.)
VocAlgorithm_SIGMOID_K                                   = (-0.0065)
VocAlgorithm_SIGMOID_X0                                  = (213.)
VocAlgorithm_VOC_INDEX_OFFSET_DEFAULT                    = (100.)
VocAlgorithm_LP_TAU_FAST                                 = (20.0)
VocAlgorithm_LP_TAU_SLOW                                 = (500.0)
VocAlgorithm_LP_ALPHA                                    = (-0.2)
VocAlgorithm_PERSISTENCE_UPTIME_GAMMA                    = ((3. * 3600.))
VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING      = (64.)
VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__FIX16_MAX          = (32767.)
FIX16_MAXIMUM                                            = 0x7FFFFFFF
FIX16_MINIMUM                                            = 0x80000000
FIX16_OVERFLOW                                           = 0x80000000
FIX16_ONE                                                = 0x00010000

class VocAlgorithmParams:
    def __init__(self):
        self.mVoc_Index_Offset = 0
        self.mTau_Mean_Variance_Hours = 0
        self.mGating_Max_Duration_Minutes = 0
        self.mSraw_Std_Initial=0
        self.mUptime=0
        self.mSraw=0
        self.mVoc_Index=0
        self.m_Mean_Variance_Estimator__Gating_Max_Duration_Minutes=0
        self.m_Mean_Variance_Estimator___Initialized=0
        self.m_Mean_Variance_Estimator___Mean=0
        self.m_Mean_Variance_Estimator___Sraw_Offset=0
        self.m_Mean_Variance_Estimator___Std=0
        self.m_Mean_Variance_Estimator___Gamma=0
        self.m_Mean_Variance_Estimator___Gamma_Initial_Mean=0
        self.m_Mean_Variance_Estimator___Gamma_Initial_Variance=0
        self.m_Mean_Variance_Estimator__Gamma_Mean=0
        self.m_Mean_Variance_Estimator__Gamma_Variance=0
        self.m_Mean_Variance_Estimator___Uptime_Gamma=0
        self.m_Mean_Variance_Estimator___Uptime_Gating=0
        self.m_Mean_Variance_Estimator___Gating_Duration_Minutes=0
        self.m_Mean_Variance_Estimator___Sigmoid__L=0
        self.m_Mean_Variance_Estimator___Sigmoid__K=0
        self.m_Mean_Variance_Estimator___Sigmoid__X0=0
        self.m_Mox_Model__Sraw_Std=3276800
        self.m_Mox_Model__Sraw_Mean=0
        self.m_Sigmoid_Scaled__Offset=0
        self.m_Adaptive_Lowpass__A1=0
        self.m_Adaptive_Lowpass__A2=0
        self.m_Adaptive_Lowpass___Initialized=0
        self.m_Adaptive_Lowpass___X1=0
        self.m_Adaptive_Lowpass___X2=0
        self.m_Adaptive_Lowpass___X3=0

class VocAlgorithm:
    
    def __init__(self):
        self.params = VocAlgorithmParams()
    def _F16(self,x):
        if x >= 0:
            return int((x)*65536.0 + 0.5)
        else:
            return int((x)*65536.0 - 0.5)

    def _fix16_from_int(self,a):
        return int(a * FIX16_ONE)

    def _fix16_cast_to_int(self,a):
        return int(a) >> 16

    def _fix16_mul(self,inArg0,inArg1):
        inArg0=int(inArg0)
        inArg1=int(inArg1)
        A = (inArg0 >> 16)
        if inArg0<0:
            B = (inArg0&0xFFFFFFFF) & 0xFFFF
        else:
            B = inArg0&0xFFFF
        C = (inArg1 >> 16)
        if inArg1<0:
            D = (inArg1&0xFFFFFFFF) & 0xFFFF
        else:
            D = inArg1&0xFFFF
        AC = (A * C)
        AD_CB = (A * D + C * B)
        BD = (B * D)
        product_hi = (AC + (AD_CB >> 16))
        ad_cb_temp = ((AD_CB) << 16)&0xFFFFFFFF
        product_lo = ((BD + ad_cb_temp))&0xFFFFFFFF
        if product_lo < BD :
            product_hi =product_hi+1
        if ((product_hi >> 31) != (product_hi >>15)):
            return FIX16_OVERFLOW
        product_lo_tmp = product_lo&0xFFFFFFFF
        product_lo = (product_lo - 0x8000)&0xFFFFFFFF
        product_lo = (product_lo-((product_hi&0xFFFFFFFF) >> 31))&0xFFFFFFFF
        if product_lo > product_lo_tmp:
            product_hi = product_hi-1
        result = (product_hi << 16)|(product_lo >> 16)
        result +=1
        return result
    
    def _fix16_div(self,a, b):
        a=int(a)
        b=int(b)
        if b==0 :
            return FIX16_MINIMUM
        if a>=0:
            remainder = a
        else:
            remainder = (a*(-1))&0xFFFFFFFF
        if b >= 0:
            divider = b
        else:
            divider = (b*(-1))&0xFFFFFFFF
        quotient = 0
        bit =0x10000
        while (divider < remainder):
            divider = divider<<1
            bit <<= 1
        if not bit:
            return FIX16_OVERFLOW
        if (divider & 0x80000000):
            if (remainder >= divider):
                quotient |= bit
                remainder -= divider
            divider >>= 1
            bit >>= 1
        while bit and remainder:
            if (remainder >= divider):
                quotient |= bit    
                remainder -= divider
            remainder <<= 1
            bit >>= 1
        if (remainder >= divider):
            quotient+=1
        result = quotient
        if ((a ^ b) & 0x80000000):
            if (result == FIX16_MINIMUM):
                return FIX16_OVERFLOW
            result = -result
        return result
    
    def _fix16_sqrt(self,x):
        x=int(x)
        num=x&0xFFFFFFFF
        result = 0
        bit = 1 << 30
        while (bit > num):
            bit >>=2
        for n in range(0,2):
            while (bit):
                if (num >= result + bit):
                    num = num-(result + bit)&0xFFFFFFFF
                    result = (result >> 1) + bit
                else:
                    result = (result >> 1)
                bit >>= 2
            if n==0:
                if num > 65535:
                    num = (num -result)&0xFFFFFFFF
                    num = ((num << 16) - 0x8000)&0xFFFFFFFF
                    result = ((result << 16) + 0x8000)&0xFFFFFFFF
                else:
                    num = ((num << 16)&0xFFFFFFFF)
                    result =((result << 16)&0xFFFFFFFF)
                bit = 1 << 14
        if (num > result):
                result+=1
        return result
    
    def _fix16_exp(self,x):
        x=int(x)
        exp_pos_values=[self._F16(2.7182818), self._F16(1.1331485), self._F16(1.0157477), self._F16(1.0019550)]
        exp_neg_values=[self._F16(0.3678794), self._F16(0.8824969), self._F16(0.9844964), self._F16(0.9980488)]
        if (x >= self._F16(10.3972)):
            return FIX16_MAXIMUM
        if (x <= self._F16(-11.7835)):
            return 0
        if (x < 0):
            x = -x
            exp_values = exp_neg_values
        else:
            exp_values = exp_pos_values
        res = FIX16_ONE
        arg = FIX16_ONE
        for i in range(0,4):
            while (x >= arg):
                res = self._fix16_mul(res, exp_values[i]);
                x -= arg;
            arg >>=3
        return res
    
    def VocAlgorithm_init(self):
        self.params.mVoc_Index_Offset = (self._F16(VocAlgorithm_VOC_INDEX_OFFSET_DEFAULT))
        self.params.mTau_Mean_Variance_Hours = self._F16(VocAlgorithm_TAU_MEAN_VARIANCE_HOURS)
        self.params.mGating_Max_Duration_Minutes =self._F16(VocAlgorithm_GATING_MAX_DURATION_MINUTES)
        self.params.mSraw_Std_Initial = self._F16(VocAlgorithm_SRAW_STD_INITIAL)
        self.params.mUptime = self._F16(0.)
        self.params.mSraw = self._F16(0.)
        self.params.mVoc_Index = 0
        self._VocAlgorithm__init_instances()
    
    def _VocAlgorithm__init_instances(self):
        self._VocAlgorithm__mean_variance_estimator__init()
        self._VocAlgorithm__mean_variance_estimator__set_parameters(self._F16(VocAlgorithm_SRAW_STD_INITIAL), self.params.mTau_Mean_Variance_Hours,self.params.mGating_Max_Duration_Minutes)
        self._VocAlgorithm__mox_model__init()
        self._VocAlgorithm__mox_model__set_parameters(self._VocAlgorithm__mean_variance_estimator__get_std(),self._VocAlgorithm__mean_variance_estimator__get_mean())
        self._VocAlgorithm__sigmoid_scaled__init()
        self._VocAlgorithm__sigmoid_scaled__set_parameters(self.params.mVoc_Index_Offset)
        self._VocAlgorithm__adaptive_lowpass__init()
        self._VocAlgorithm__adaptive_lowpass__set_parameters()
    
    def _VocAlgorithm_get_states(self,state0,state1):
        state0 = self._VocAlgorithm__mean_variance_estimator__get_mean()
        state1 = _VocAlgorithm__mean_variance_estimator__get_std()
        return state0,state1
    
    def _VocAlgorithm_set_states(self,state0,state1):
        self._VocAlgorithm__mean_variance_estimator__set_states(params, state0, state1, self._F16(VocAlgorithm_PERSISTENCE_UPTIME_GAMMA))
        self.params.mSraw = state0
    
    def _VocAlgorithm_set_tuning_parameters(self, voc_index_offset, learning_time_hours, gating_max_duration_minutes, std_initial):
        self.params.mVoc_Index_Offset = self._fix16_from_int(voc_index_offset)
        self.params.mTau_Mean_Variance_Hours = self._fix16_from_int(learning_time_hours)
        self.params.mGating_Max_Duration_Minutes =self._fix16_from_int(gating_max_duration_minutes)
        self.params.mSraw_Std_Initial = self._fix16_from_int(std_initial)
        self._VocAlgorithm__init_instances();
    
    def VocAlgorithm_process(self, sraw):
        if ((self.params.mUptime <= self._F16(VocAlgorithm_INITIAL_BLACKOUT))):
            self.params.mUptime = self.params.mUptime + self._F16(VocAlgorithm_SAMPLING_INTERVAL)
        else:
            if (((sraw > 0) and (sraw < 65000))):
                if ((sraw < 20001)):
                    sraw = 20001
                elif((sraw > 52767)):
                    sraw = 52767
                self.params.mSraw = self._fix16_from_int((sraw - 20000))
            self.params.mVoc_Index =self._VocAlgorithm__mox_model__process(self.params.mSraw)
            self.params.mVoc_Index =self._VocAlgorithm__sigmoid_scaled__process(self.params.mVoc_Index)
            self.params.mVoc_Index =self._VocAlgorithm__adaptive_lowpass__process(self.params.mVoc_Index)
            if ((self.params.mVoc_Index < self._F16(0.5))):
                self.params.mVoc_Index = self._F16(0.5)
            if self.params.mSraw > self._F16(0.):
                self._VocAlgorithm__mean_variance_estimator__process(self.params.mSraw, self.params.mVoc_Index)
                self._VocAlgorithm__mox_model__set_parameters(self._VocAlgorithm__mean_variance_estimator__get_std(),self._VocAlgorithm__mean_variance_estimator__get_mean())
        voc_index = self._fix16_cast_to_int((self.params.mVoc_Index + self._F16(0.5))) 
        return voc_index
    
    def _VocAlgorithm__mean_variance_estimator__init(self):
        self._VocAlgorithm__mean_variance_estimator__set_parameters(self._F16(0.),self._F16(0.),self._F16(0.))
        self._VocAlgorithm__mean_variance_estimator___init_instances()
    
    def _VocAlgorithm__mean_variance_estimator___init_instances(self):
        self._VocAlgorithm__mean_variance_estimator___sigmoid__init()
    
    def _VocAlgorithm__mean_variance_estimator__set_parameters(self, std_initial, tau_mean_variance_hours, gating_max_duration_minutes):
        self.params.m_Mean_Variance_Estimator__Gating_Max_Duration_Minutes = gating_max_duration_minutes
        self.params.m_Mean_Variance_Estimator___Initialized = 0
        self.params.m_Mean_Variance_Estimator___Mean = self._F16(0.)
        self.params.m_Mean_Variance_Estimator___Sraw_Offset = self._F16(0.)
        self.params.m_Mean_Variance_Estimator___Std = std_initial
        self.params.m_Mean_Variance_Estimator___Gamma =self._fix16_div(self._F16((VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *(VocAlgorithm_SAMPLING_INTERVAL / 3600.))\
                                                                                  ),(tau_mean_variance_hours +self._F16((VocAlgorithm_SAMPLING_INTERVAL / 3600.))))
        self.params.m_Mean_Variance_Estimator___Gamma_Initial_Mean =self._F16(((VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *VocAlgorithm_SAMPLING_INTERVAL) \
                                                                                /(VocAlgorithm_TAU_INITIAL_MEAN + VocAlgorithm_SAMPLING_INTERVAL)))
        self.params.m_Mean_Variance_Estimator___Gamma_Initial_Variance = self._F16(((VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *VocAlgorithm_SAMPLING_INTERVAL) \
                                                                                     /(VocAlgorithm_TAU_INITIAL_VARIANCE + VocAlgorithm_SAMPLING_INTERVAL)))
        self.params.m_Mean_Variance_Estimator__Gamma_Mean = self._F16(0.)
        self.params.m_Mean_Variance_Estimator__Gamma_Variance = self._F16(0.)
        self.params.m_Mean_Variance_Estimator___Uptime_Gamma = self._F16(0.)
        self.params.m_Mean_Variance_Estimator___Uptime_Gating = self._F16(0.)
        self.params.m_Mean_Variance_Estimator___Gating_Duration_Minutes = self._F16(0.)
    
    def _VocAlgorithm__mean_variance_estimator__set_states(self, mean, std, uptime_gamma):
        self.params.m_Mean_Variance_Estimator___Mean = mean
        self.params.m_Mean_Variance_Estimator___Std = std
        self.params.m_Mean_Variance_Estimator___Uptime_Gamma = uptime_gamma
        self.params.m_Mean_Variance_Estimator___Initialized = true
        
    
    def _VocAlgorithm__mean_variance_estimator__get_std(self):
        return self.params.m_Mean_Variance_Estimator___Std
    
    def _VocAlgorithm__mean_variance_estimator__get_mean(self):
        return (self.params.m_Mean_Variance_Estimator___Mean +self.params.m_Mean_Variance_Estimator___Sraw_Offset)
    
    def _VocAlgorithm__mean_variance_estimator___calculate_gamma(self, voc_index_from_prior):
        uptime_limit = self._F16((VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__FIX16_MAX -VocAlgorithm_SAMPLING_INTERVAL))
        if self.params.m_Mean_Variance_Estimator___Uptime_Gamma < uptime_limit:
            self.params.m_Mean_Variance_Estimator___Uptime_Gamma =(self.params.m_Mean_Variance_Estimator___Uptime_Gamma +self._F16(VocAlgorithm_SAMPLING_INTERVAL))
        
        if self.params.m_Mean_Variance_Estimator___Uptime_Gating < uptime_limit:
            self.params.m_Mean_Variance_Estimator___Uptime_Gating =(self.params.m_Mean_Variance_Estimator___Uptime_Gating +self._F16(VocAlgorithm_SAMPLING_INTERVAL))
        
        self._VocAlgorithm__mean_variance_estimator___sigmoid__set_parameters(self._F16(1.), self._F16(VocAlgorithm_INIT_DURATION_MEAN),self._F16(VocAlgorithm_INIT_TRANSITION_MEAN))
        sigmoid_gamma_mean =self._VocAlgorithm__mean_variance_estimator___sigmoid__process(self.params.m_Mean_Variance_Estimator___Uptime_Gamma)
        gamma_mean =(self.params.m_Mean_Variance_Estimator___Gamma +(self._fix16_mul((self.params.m_Mean_Variance_Estimator___Gamma_Initial_Mean -self.params.m_Mean_Variance_Estimator___Gamma),sigmoid_gamma_mean)))
        gating_threshold_mean =(self._F16(VocAlgorithm_GATING_THRESHOLD)\
                                +(self._fix16_mul(self._F16((VocAlgorithm_GATING_THRESHOLD_INITIAL -VocAlgorithm_GATING_THRESHOLD)),\
                                 self._VocAlgorithm__mean_variance_estimator___sigmoid__process(self.params.m_Mean_Variance_Estimator___Uptime_Gating))))
        self._VocAlgorithm__mean_variance_estimator___sigmoid__set_parameters(self._F16(1.),gating_threshold_mean,self._F16(VocAlgorithm_GATING_THRESHOLD_TRANSITION))
        
        sigmoid_gating_mean =self._VocAlgorithm__mean_variance_estimator___sigmoid__process(voc_index_from_prior)
        self.params.m_Mean_Variance_Estimator__Gamma_Mean =(self._fix16_mul(sigmoid_gating_mean, gamma_mean))
        
        self._VocAlgorithm__mean_variance_estimator___sigmoid__set_parameters(self._F16(1.), self._F16(VocAlgorithm_INIT_DURATION_VARIANCE),self._F16(VocAlgorithm_INIT_TRANSITION_VARIANCE))
        
        sigmoid_gamma_variance =self._VocAlgorithm__mean_variance_estimator___sigmoid__process( self.params.m_Mean_Variance_Estimator___Uptime_Gamma)
        
        gamma_variance =(self.params.m_Mean_Variance_Estimator___Gamma +\
                        (self._fix16_mul((self.params.m_Mean_Variance_Estimator___Gamma_Initial_Variance \
                                          -self.params.m_Mean_Variance_Estimator___Gamma),\
                                          (sigmoid_gamma_variance - sigmoid_gamma_mean))))
        
        gating_threshold_variance =(self._F16(VocAlgorithm_GATING_THRESHOLD) \
                                    +(self._fix16_mul(self._F16((VocAlgorithm_GATING_THRESHOLD_INITIAL -VocAlgorithm_GATING_THRESHOLD)),\
                                     self._VocAlgorithm__mean_variance_estimator___sigmoid__process( self.params.m_Mean_Variance_Estimator___Uptime_Gating))))
        
        self._VocAlgorithm__mean_variance_estimator___sigmoid__set_parameters(self._F16(1.), gating_threshold_variance,self._F16(VocAlgorithm_GATING_THRESHOLD_TRANSITION))
        
        sigmoid_gating_variance =self._VocAlgorithm__mean_variance_estimator___sigmoid__process( voc_index_from_prior)
        
        self.params.m_Mean_Variance_Estimator__Gamma_Variance =(self._fix16_mul(sigmoid_gating_variance, gamma_variance))
        
        self.params.m_Mean_Variance_Estimator___Gating_Duration_Minutes =(self.params.m_Mean_Variance_Estimator___Gating_Duration_Minutes \
                                                                          +(self._fix16_mul(self._F16((VocAlgorithm_SAMPLING_INTERVAL / 60.)),\
                                                                                           ((self._fix16_mul((self._F16(1.) - sigmoid_gating_mean),\
                                                                                                             self._F16((1. + VocAlgorithm_GATING_MAX_RATIO))))\
                                                                                              -self._F16(VocAlgorithm_GATING_MAX_RATIO)))))
        
        if ((self.params.m_Mean_Variance_Estimator___Gating_Duration_Minutes <self._F16(0.))):
            self.params.m_Mean_Variance_Estimator___Gating_Duration_Minutes = self._F16(0.)
        
        if ((self.params.m_Mean_Variance_Estimator___Gating_Duration_Minutes >self.params.m_Mean_Variance_Estimator__Gating_Max_Duration_Minutes)):
            self.params.m_Mean_Variance_Estimator___Uptime_Gating = self._F16(0.)
    
    def _VocAlgorithm__mean_variance_estimator__process(self, sraw, voc_index_from_prior):
        if ((self.params.m_Mean_Variance_Estimator___Initialized == 0)):
            self.params.m_Mean_Variance_Estimator___Initialized = 1
            self.params.m_Mean_Variance_Estimator___Sraw_Offset = sraw
            self.params.m_Mean_Variance_Estimator___Mean = self._F16(0.)
        else:
            if (((self.params.m_Mean_Variance_Estimator___Mean >= self._F16(100.)) or (self.params.m_Mean_Variance_Estimator___Mean <= self._F16(-100.)))):
                self.params.m_Mean_Variance_Estimator___Sraw_Offset =(self.params.m_Mean_Variance_Estimator___Sraw_Offset +self.params.m_Mean_Variance_Estimator___Mean)
                self.params.m_Mean_Variance_Estimator___Mean = self._F16(0.)
            
            sraw = (sraw - self.params.m_Mean_Variance_Estimator___Sraw_Offset)
            self._VocAlgorithm__mean_variance_estimator___calculate_gamma( voc_index_from_prior)
            delta_sgp = (self._fix16_div((sraw - self.params.m_Mean_Variance_Estimator___Mean),self._F16(VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING)))
            if ((delta_sgp < self._F16(0.))):
                c = (self.params.m_Mean_Variance_Estimator___Std - delta_sgp)
            else:
                c = (self.params.m_Mean_Variance_Estimator___Std + delta_sgp)
            additional_scaling = self._F16(1.)
            if ((c > self._F16(1440.))):
                additional_scaling = self._F16(4.)
            self.params.m_Mean_Variance_Estimator___Std = self._fix16_mul(self._fix16_sqrt((self._fix16_mul(additional_scaling,\
                                                                                          (self._F16(VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING) -self.params.m_Mean_Variance_Estimator__Gamma_Variance)))),\
                                                                          self._fix16_sqrt(((self._fix16_mul(self.params.m_Mean_Variance_Estimator___Std,\
                                                                                                            (self._fix16_div(self.params.m_Mean_Variance_Estimator___Std,\
                                                                                                            (self._fix16_mul(self._F16(VocAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING),additional_scaling)))))) \
                                                                                          +(self._fix16_mul((self._fix16_div((self._fix16_mul(self.params.m_Mean_Variance_Estimator__Gamma_Variance,delta_sgp)),additional_scaling))\
                                                                                          ,delta_sgp)))))
            self.params.m_Mean_Variance_Estimator___Mean =(self.params.m_Mean_Variance_Estimator___Mean +(self._fix16_mul(self.params.m_Mean_Variance_Estimator__Gamma_Mean,delta_sgp)))
    
    def _VocAlgorithm__mean_variance_estimator___sigmoid__init(self):
        self._VocAlgorithm__mean_variance_estimator___sigmoid__set_parameters(self._F16(0.), self._F16(0.), self._F16(0.))
    
    def _VocAlgorithm__mean_variance_estimator___sigmoid__set_parameters(self, L, X0, K):
        self.params.m_Mean_Variance_Estimator___Sigmoid__L = L;
        self.params.m_Mean_Variance_Estimator___Sigmoid__K = K;        
        self.params.m_Mean_Variance_Estimator___Sigmoid__X0 = X0;        
    
    def _VocAlgorithm__mean_variance_estimator___sigmoid__process(self, sample):
        x = (self._fix16_mul(self.params.m_Mean_Variance_Estimator___Sigmoid__K,(sample - self.params.m_Mean_Variance_Estimator___Sigmoid__X0)))
        if ((x < self._F16(-50.))):
            return self.params.m_Mean_Variance_Estimator___Sigmoid__L
        elif ((x > self._F16(50.))):
            return self._F16(0.)
        else:
            return (self._fix16_div(self.params.m_Mean_Variance_Estimator___Sigmoid__L,(self._F16(1.) + self._fix16_exp(x))))
    
    def _VocAlgorithm__mox_model__init(self):
        self._VocAlgorithm__mox_model__set_parameters(self._F16(1.),self._F16(0.))
    
    def _VocAlgorithm__mox_model__set_parameters(self,SRAW_STD,SRAW_MEAN):
        self.params.m_Mox_Model__Sraw_Std = SRAW_STD;
        self.params.m_Mox_Model__Sraw_Mean = SRAW_MEAN;        
    
    def _VocAlgorithm__mox_model__process(self,sraw):
        return (self._fix16_mul((self._fix16_div((sraw - self.params.m_Mox_Model__Sraw_Mean),(-(self.params.m_Mox_Model__Sraw_Std +self._F16(VocAlgorithm_SRAW_STD_BONUS))))),self._F16(VocAlgorithm_VOC_INDEX_GAIN)))
    
    def _VocAlgorithm__sigmoid_scaled__init(self):
        self._VocAlgorithm__sigmoid_scaled__set_parameters(self._F16(0.))
    
    def _VocAlgorithm__sigmoid_scaled__set_parameters(self,offset):
        self.params.m_Sigmoid_Scaled__Offset = offset
    
    def _VocAlgorithm__sigmoid_scaled__process(self,sample):
        x = (self._fix16_mul(self._F16(VocAlgorithm_SIGMOID_K),(sample - self._F16(VocAlgorithm_SIGMOID_X0))))
        if ((x < self._F16(-50.))):
            return self._F16(VocAlgorithm_SIGMOID_L)
        elif ((x > self._F16(50.))):
            return self._F16(0.)
        else:
            if ((sample >= self._F16(0.))):
                shift = (self._fix16_div((self._F16(VocAlgorithm_SIGMOID_L) -(self._fix16_mul(self._F16(5.), self.params.m_Sigmoid_Scaled__Offset))),self._F16(4.)))
                return ((self._fix16_div((self._F16(VocAlgorithm_SIGMOID_L) + shift),(self._F16(1.) + self._fix16_exp(x)))) -shift)
            else:
                return (self._fix16_mul((self._fix16_div(self.params.m_Sigmoid_Scaled__Offset,self._F16(VocAlgorithm_VOC_INDEX_OFFSET_DEFAULT))),\
                                         (self._fix16_div(self._F16(VocAlgorithm_SIGMOID_L),(self._F16(1.) + self._fix16_exp(x))))))
    
    def _VocAlgorithm__adaptive_lowpass__init(self):
        self._VocAlgorithm__adaptive_lowpass__set_parameters()
    
    def _VocAlgorithm__adaptive_lowpass__set_parameters(self):
        self.params.m_Adaptive_Lowpass__A1 =self._F16((VocAlgorithm_SAMPLING_INTERVAL /(VocAlgorithm_LP_TAU_FAST + VocAlgorithm_SAMPLING_INTERVAL)))
        self.params.m_Adaptive_Lowpass__A2 =self._F16((VocAlgorithm_SAMPLING_INTERVAL /(VocAlgorithm_LP_TAU_SLOW + VocAlgorithm_SAMPLING_INTERVAL)))
        self.params.m_Adaptive_Lowpass___Initialized = 0
    
    def _VocAlgorithm__adaptive_lowpass__process(self,sample):
        if ((self.params.m_Adaptive_Lowpass___Initialized == 0)):
            self.params.m_Adaptive_Lowpass___X1 = sample;
            self.params.m_Adaptive_Lowpass___X2 = sample;
            self.params.m_Adaptive_Lowpass___X3 = sample;
            self.params.m_Adaptive_Lowpass___Initialized = 1;
        self.params.m_Adaptive_Lowpass___X1 =((self._fix16_mul((self._F16(1.) - self.params.m_Adaptive_Lowpass__A1),self.params.m_Adaptive_Lowpass___X1)) +(self._fix16_mul(self.params.m_Adaptive_Lowpass__A1, sample)))
        
        self.params.m_Adaptive_Lowpass___X2 =((self._fix16_mul((self._F16(1.) - self.params.m_Adaptive_Lowpass__A2),self.params.m_Adaptive_Lowpass___X2)) +(self._fix16_mul(self.params.m_Adaptive_Lowpass__A2, sample)))
        
        abs_delta =(self.params.m_Adaptive_Lowpass___X1 - self.params.m_Adaptive_Lowpass___X2)
        
        if ((abs_delta < self._F16(0.))):
            abs_delta = (-abs_delta)
        F1 = self._fix16_exp((self._fix16_mul(self._F16(VocAlgorithm_LP_ALPHA), abs_delta)))
        tau_a =((self._fix16_mul(self._F16((VocAlgorithm_LP_TAU_SLOW - VocAlgorithm_LP_TAU_FAST)),F1)) +self._F16(VocAlgorithm_LP_TAU_FAST))
        a3 = (self._fix16_div(self._F16(VocAlgorithm_SAMPLING_INTERVAL),(self._F16(VocAlgorithm_SAMPLING_INTERVAL) + tau_a)))
        self.params.m_Adaptive_Lowpass___X3 =((self._fix16_mul((self._F16(1.) - a3), self.params.m_Adaptive_Lowpass___X3)) +(self._fix16_mul(a3, sample)))
        return self.params.m_Adaptive_Lowpass___X3