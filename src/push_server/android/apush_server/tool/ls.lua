--[[
本脚本用于loginserver相关消息的解析，可以解析：
    1.加密的loginv1、heartbeatv1、fluxreportv1、logoutv1及其响应消息。
--]]

do
    --Proto用来注册新协议
	local p_ls = Proto("LS","login server")

	--ProtoField.***定义将在包详细信息面板显示的字段
    local f_res3 = ProtoField.uint24("ls.res3","Reserved",base.HEX)
    local f_res2 = ProtoField.uint16("ls.res2","Reserved",base.HEX)
	local f_res4 = ProtoField.uint32("ls.res4","Reserved",base.HEX)
	local f_randkey = ProtoField.uint16("ls.randkey","Random Key",base.HEX)
	local f_seckeyindex = ProtoField.uint8("ls.randkey","secret Key index",base.HEX,nil,0xf0)
	local f_algver = ProtoField.uint8("ls.algver","Algrithm Version",base.HEX,nil,0x0f)
	local f_enlen = ProtoField.uint8("ls.enlen","Encrypted Length",base.DEC)
    local f_len = ProtoField.uint32("ls.len","Length",base.DEC)
    local f_type = ProtoField.uint16("ls.type","Type",base.HEX,{ [0x0286] = "pausetime report response",[0x0206] = "pausetime report",[0x0285] = "bufftime report response",[0x0205] = "bufftime report",[0x0287] = "relogin", [0x0201] = "login", [0x0281] = "login response",[0x0202] = "logout", [0x0203] = "heartbeat",[0x0283] = "heartbeat response",[0x0204] = "flux report",[0x0284] = "flux report response"})
    local f_pver = ProtoField.uint16("ls.pver","Protocol Version",base.HEX)
    local f_sid = ProtoField.uint16("ls.sid","Session ID",base.HEX)
	local f_chksum = ProtoField.uint16("ls.chksum","Checksum",base.HEX)
    local f_res1 = ProtoField.uint8("ls.res1","Reserved",base.HEX)
    local f_peerid = ProtoField.bytes("ls.peerid","peerid",base.HEX)
    local f_cver = ProtoField.ipv4("ls.cver","client version",base.HEX)
    local f_chanid = ProtoField.uint32("ls.chanid","channel id",base.HEX)
    local f_pip = ProtoField.ipv4("ls.pip","Private IP")
    local f_pport = ProtoField.uint16("ls.pport","Private Port",base.DEC)
    local f_mac = ProtoField.ether("ls.mac","Mac Addres1")
    local f_nat = ProtoField.uint8("ls.nat","NAT Type",base.HEX,{ [0x00]= "nt_reserved",[0x01]	= "nt_cone",[0x02] = "nt_symmetric_positive",[0x03] = "nt_public",[0x04] = "nt_symmetric_negative",[0x06] = "nt_portmapping",[0x08]	= "nt_upnp",[0x09] = "nt_unrestrict_cone",[0x0a] = "nt_unrestrict_symmetric_positive",[0x0b] = "nt_unrestrict_symmetric_negative"})
    local f_uifs = ProtoField.uint8("ls.uifs","UI&fs",base.DEC,{ [1] = "UI and funshionservice all running",[0] = "only funshionservice is running"})
    local f_loc = ProtoField.uint16("ls.loc","Location",base.HEX)
	local f_hbt = ProtoField.uint8("ls.hbr","Heartbeat Retry Times")
	local f_hbi = ProtoField.uint16("ls.hbi","Heartbeat Interval")
    local f_fluxi = ProtoField.uint16("ls.fluxi","Flux Report Interval")
	local f_ackcmd = ProtoField.uint32("ls.ackcmd","ACK_CMD",base.HEX)
	local f_cmd = ProtoField.uint32("ls.cmd","CMD",base.HEX)
	local f_runtime = ProtoField.uint32("ls.runtime","Runtime")
	local f_uflux = ProtoField.uint64("ls.uflux","Upload Flux",base.DEC)
	local f_dflux = ProtoField.uint64("ls.dflux","Download Flux")
	local f_random = ProtoField.bytes("ls.random","Random Data",base.HEX)
	local f_locnum = ProtoField.uint16("ls.locnum","Location Number",base.DEC)
	local f_desloc = ProtoField.uint16("ls.desloc","Destination Location",base.DEC)
	local f_uflux4 = ProtoField.uint64("ls.uflux4","Upload Flux",base.DEC)
	local f_dflux4 = ProtoField.uint64("ls.dflux4","Download Flux",base.DEC)
	local f_taskid = ProtoField.bytes("ls.taskid","taskid",base.HEX)
	local f_bufftime = ProtoField.uint16("ls.bufftime","bufftime",base.DEC)
	local f_dspeed = ProtoField.uint16("ls.dspeed","Download Speed",base.DEC)
	local f_paustime = ProtoField.uint16("ls.paustime","Pause Time",base.DEC)



    -- 前面定义的字段，需要通过p_heartbeat.fields注册才能在包详细信息面板中显示出来
    p_ls.fields = {f_paustime,f_bufftime,f_dspeed,f_taskid,f_uflux4,f_dflux4,f_locnum,f_desloc,f_randkey,f_seckeyindex,f_algver,f_enlen,f_res2,f_random,f_hbt,f_hbi,f_fluxi,f_ackcmd,f_cmd,f_runtime,f_uflux,f_dflux,f_res1,f_res4,f_peerid,f_cver,f_chanid,f_pip,f_pport,f_mac,f_nat,f_uifs,f_res3,f_len,f_type,f_pver,f_sid,f_loc,f_chksum}


    local function loginv1_dissector(buf,pinfo,t)
	    local buf_len = buf:len()
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(2,1))
		t:add(f_enlen,buf(3,1)):append_text(" bytes")
		t:add(f_len,buf(4,4)):append_text(" bytes")
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
		t:add(f_peerid,buf(16,20))
		t:add(f_cver,buf(36,4))
		t:add(f_chanid,buf(40,4))
		t:add(f_pip,buf(44,4))
		t:add(f_pport,buf(48,2))
		t:add(f_mac,buf(50,6))
		t:add(f_nat,buf(56,1))
		t:add(f_uifs,buf(57,1))
		local rnum = buf_len - 58
		if rnum > 0 then
            t:add(f_random,buf(58,rnum))
		end
    	pinfo.cols.info="Login V1 Message"
    end


    local function loginrespv1_dissector(buf,pinfo,t)
	    local buf_len = buf:len()
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(2,1))
		t:add(f_enlen,buf(3,1)):append_text(" bytes")
		t:add(f_len,buf(4,4)):append_text(" bytes")
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
		t:add(f_loc,buf(16,2))
		t:add(f_hbi,buf(18,2))
		t:add(f_hbt,buf(20,1))
		t:add(f_res1,buf(21,1))
		t:add(f_fluxi,buf(22,2)):append_text(" s")
		local rnum = buf_len - 24
		if rnum > 0 then
            t:add(f_random,buf(24,rnum))
		end
    	pinfo.cols.info="Login V1 response Message"
    end


    local function logoutv1_dissector(buf,pinfo,t)
	    local buf_len = buf:len()
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(2,1))
		t:add(f_enlen,buf(3,1)):append_text(" bytes")
		t:add(f_len,buf(4,4)):append_text(" bytes")
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
		t:add(f_peerid,buf(16,20))
		local rnum = buf_len-36
		if rnum > 0 then
            t:add(f_random,buf(36,rnum))
		end
        pinfo.cols.info="Logout V1 Message"
    end


    local function heartbeatv1_dissector(buf,pinfo,t)
		local t=t:add(buf(0,-1),"Heartbeat V1 message")
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(2,1))
		t:add(f_enlen,buf(3,1)):append_text(" bytes")
		t:add(f_len,buf(4,4)):append_text(" bytes")
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
		t:add(f_peerid,buf(16,20))
		t:add(f_uifs,buf(36,1))
		t:add(f_res3,buf(37,3))
		local offset = 40
		local buf_len = buf:len()
		local n = math.floor((buf_len - offset)/4)
		for i=1,n do
		    t:add(f_ackcmd,buf(offset,4))
			offset = offset + 4
		end

    	pinfo.cols.info="Heartbeat V1 Message"
    end

    local function heartbeatrespv1_dissector(buf,pinfo,t)
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(2,1))
		t:add(f_enlen,buf(3,1)):append_text(" bytes")
		t:add(f_len,buf(4,4)):append_text(" bytes")
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
		local offset = 16
		local buf_len = buf:len()
		local n = math.floor((buf_len - offset)/8)
		for i=1,n do
		    t:add(f_cmd,buf(offset,4))
			t:add(f_runtime,buf(offset+4,4))
			offset = offset + 8
		end
		local rnum = buf_len%8
		if rnum > 0 then
            t:add(f_random,buf(offset,rnum))
		end

    	pinfo.cols.info="Heartbeat V1 Response Message"
    end

    local function fluxreportv1_dissector(buf,pinfo,t)
	    local buf_len = buf:len()
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(2,1))
		t:add(f_enlen,buf(3,1)):append_text(" bytes")
		t:add(f_len,buf(4,4)):append_text(" bytes")
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
        t:add(f_uflux,buf(16,8)):append_text(" MB")
		t:add(f_dflux,buf(24,8)):append_text(" MB")
		t:add(f_peerid,buf(32,20))
		local rnum = buf_len - 52
		if rnum > 0 then
            t:add(f_random,buf(52,rnum))
		end
    	pinfo.cols.info="Flux Report V1 Message"
    end


-------------------flux report v2 ------------------
    local function fluxreportv2_dissector(buf,pinfo,t)
	    local buf_len = buf:len()
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(2,1))
		t:add(f_enlen,buf(3,1)):append_text(" bytes")
		t:add(f_len,buf(4,4)):append_text(" bytes")
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
		t:add(f_peerid,buf(16,20))
		local uflux = buf(36,4):uint() /1024
		local dflux = buf(40,4):uint() /1024
        t:add(f_uflux,buf(36,4)):append_text(" KB = ".. uflux .." MB")
		t:add(f_dflux,buf(40,4)):append_text(" KB = ".. dflux .." MB")
		t:add(f_locnum,buf(44,2))
		local locnum = buf(44,2):uint()
		local offset = 46
		for i=1,locnum do
		    t:add(f_desloc,buf(offset,2))
		    t:add(f_dflux,buf(offset+2,4)):append_text(" KB")
			offset = offset +6
		end

    	pinfo.cols.info="Flux Report V2 Message"
    end

-------------------buff time report v1 ------------------
    local function bufftimereportv1_dissector(buf,pinfo,t)
	    local buf_len = buf:len()
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(2,1))
		t:add(f_enlen,buf(3,1)):append_text(" bytes")
		t:add(f_len,buf(4,4)):append_text(" bytes")
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
		t:add(f_peerid,buf(16,20))
		t:add(f_taskid,buf(36,20))
		t:add(f_bufftime,buf(56,2)):append_text(" s")
		t:add(f_dspeed,buf(58,2)):append_text(" kB/s")
		t:add(f_res4,buf(60,4))
        local buf_len = buf:len()
		if buf_len > 64 then
            t:add(f_random,buf(64,rnum))
		end

    	pinfo.cols.info="Buff Time Report V1 Message"
    end


-------------------pause time report v1 ------------------
    local function pausetimereportv1_dissector(buf,pinfo,t)
	    local buf_len = buf:len()
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(2,1))
		t:add(f_enlen,buf(3,1)):append_text(" bytes")
		t:add(f_len,buf(4,4)):append_text(" bytes")
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
		t:add(f_peerid,buf(16,20))
		t:add(f_taskid,buf(36,20))
		t:add(f_paustime,buf(56,2)):append_text(" s")
		t:add(f_dspeed,buf(58,2)):append_text(" kB/s")
		t:add(f_res4,buf(60,4))
        local buf_len = buf:len()
		if buf_len > 64 then
            t:add(f_random,buf(64,rnum))
		end

    	pinfo.cols.info="Pause Time Report V1 Message"
    end


    local function onlyheadrespv1_dissector(buf,pinfo,t)
	    local buf_len = buf:len()
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(2,1))
		t:add(f_enlen,buf(3,1)):append_text(" bytes")
		t:add(f_len,buf(4,4)):append_text(" bytes")
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
		local rnum = buf_len%8
		if rnum > 0 then
            t:add(f_random,buf(16,rnum))
		end

    end


    -- p_ls.dissector(buf,pinfo,root)协议解析函数
	function p_ls.dissector(buf,pinfo,root)
		local buf_len = buf:len()
		local t=root:add(p_ls,buf(0,-1))

		--把原始的加密数据展现在包详细面板中
		local data_dis = Dissector.get("data")
		data_dis:call(buf,pinfo,t)

		pinfo.cols.protocol = p_ls.name

	    --解密
        local secret_key={
						0x12,0x3e,0xab,0xe3,0xab,0xc1,0xe3,0xbf,0x3b,0xef,0xab,0x98,0xef,0x2c,0x45,0xad,
	                    0x32,0xa9,0xb3,0xf8,0xeb,0x2c,0xd3,0x9d,0xdd,0xee,0x33,0xa5,0xcf,0xc2,0x79,0x8a,
	                    0x23,0xbc,0xea,0x23,0x4f,0xba,0x32,0x9a,0xab,0xc2,0x9e,0xa9,0x11,0x23,0x5a,0x6b,
						0xbc,0xe3,0x57,0xbc,0x58,0xe8,0x7d,0xf9,0xa6,0x54,0xcd,0x87,0x65,0x3a,0xef,0x98
	                     }
        local rand1 = buf(0,1):uint()
	    local rand2 = buf(1,1):uint()
	    local skeyb = bit.band(bit.rshift(buf(2,1):uint(),4),0x0f)
	    local skey_loc = skeyb*4+1
	    local n = math.floor((buf_len-4)/4)
	    local decmessage={}
	    local m=4*n
	    local lefted = buf_len-4-m
		local key3 = bit.bxor(rand2,secret_key[skey_loc+2])
		local key4 = bit.bxor(rand1,secret_key[skey_loc+3])
		local enclen = buf(3,1):uint()
		local clen = bit.bxor(enclen,key4)
		local key={secret_key[skey_loc],secret_key[skey_loc+1],key3,key4}

		for j=0,n-1 do
		    for i=1,4 do
				decmessage[j*4+i]=bit.bxor(buf(3+j*4+i,1):uint(),key[5-i])
			end
        end

        for j=1,lefted do
            decmessage[m+j] = bit.bxor(key4,buf(m+3+j,1):uint())
        end

		table.insert(decmessage,1,clen)

        for j=1,3 do
            table.insert(decmessage,1,buf(3-j,1):uint())
        end

    --解密数据转换成ByteArray类型
        local str = ''
        for i=1,buf_len do
            str = str .. string.format("%02x",decmessage[i])
        end
        local b = ByteArray.new(str)



		local tvb = b:tvb("The Decrypted Data")
		local typ = tvb(8,2):uint()
		local len = tvb(4,4):uint()
		local ver = tvb(10,2):uint()
		local sub_t=t:add(tvb(),"The Decrypted Data")

		if len == buf_len and typ == 0x0201 then
		    t:append_text(": Login V1 Message")
			loginv1_dissector(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x0281 then
		    t:append_text(": Login V1 Response Message")
		    loginrespv1_dissector(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x0202 then
		    t:append_text(": Logout V1 Message")
		    logoutv1_dissector(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x0203 then
		    t:append_text(": Heartbeat V1 Message")
		    heartbeatv1_dissector(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x0283 then
		    t:append_text(": Heartbeat V1 Response Message")
		    heartbeatrespv1_dissector(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x0204 and ver == 0x0001 then
		    t:append_text(": Flux Report V1 Message")
		    fluxreportv1_dissector(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x0204 and ver == 0x0002 then
		    t:append_text(": Flux Report V2 Message")
		    fluxreportv2_dissector(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x0205 and ver == 0x0001 then
		    t:append_text(": BuffTime Report V2 Message")
		    bufftimereportv1_dissector(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x0206 and ver == 0x0001 then
		    t:append_text(": Pause Time Report V1 Message")
		    pausetimereportv1_dissector(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x0284 and ver == 0x0001 then
		    t:append_text(": Flux Report V1 Reponse Message")
			pinfo.cols.info="Flux Report V1 Response Message"
		    onlyheadrespv1_dissector(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x0284 and ver == 0x0002 then
		    t:append_text(": Flux Report V2 Reponse Message")
			pinfo.cols.info="Flux Report V2 Response Message"
		    onlyheadrespv1_dissector(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x0287 then
		    t:append_text(": Relogin v1 Message")
			pinfo.cols.info="Relogin V1 Message"
		    onlyheadrespv1_dissector(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x0285 then
		    t:append_text(": BuffTime Report Response v1 Message")
			pinfo.cols.info="BuffTime Report Response v1 Message"
		    onlyheadrespv1_dissector(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x0286 then
		    t:append_text(": Pause Time Report Response v1 Message")
			pinfo.cols.info="Pause Time Report Response v1 Message"
		    onlyheadrespv1_dissector(tvb,pinfo,sub_t)
		end
	end

	--注册Proto的解析端口
	local udp_encap_table = DissectorTable.get("udp.port")
	      udp_encap_table:add(8080,p_ls)
		  udp_encap_table:add(9090,p_ls)
		  udp_encap_table:add(6000,p_ls)
              udp_encap_table:add(7000,p_ls)
              udp_encap_table:add(6010,p_ls)
              udp_encap_table:add(6800,p_ls)
              udp_encap_table:add(8016 ,p_ls)
              udp_encap_table:add(11230 ,p_ls)
		udp_encap_table:add(55802 ,p_ls)
		udp_encap_table:add(45535 ,p_ls)
	local tcp_encap_table = DissectorTable.get("tcp.port")
	      tcp_encap_table:add(9090,p_ls)
		  tcp_encap_table:add(7501,p_ls)
		  tcp_encap_table:add(8080,p_ls)
              tcp_encap_table:add(6000 ,p_ls)
              tcp_encap_table:add(6010 ,p_ls)
              tcp_encap_table:add(7000 ,p_ls)
              tcp_encap_table:add(6800 ,p_ls)
              tcp_encap_table:add(8016 ,p_ls)
              tcp_encap_table:add(11230 ,p_ls)
		tcp_encap_table:add(55801 ,p_ls)
              tcp_encap_table:add(45535 ,p_ls)

end

