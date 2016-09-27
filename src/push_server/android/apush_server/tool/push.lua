--[[
本脚本用于loginserver相关消息的解析，可以解析：
    1.加密的loginv1、heartbeatv1、fluxreportv1、logoutv1及其响应消息。
--]]

do
	--Proto用来注册新协议
	local p_ls = Proto("APUSH","apush")

	--ProtoField.***定义将在包详细信息面板显示的字段
	local f_res3 = ProtoField.uint24("ls.res3","Reserved",base.HEX)
	local f_res2 = ProtoField.uint16("ls.res2","Reserved",base.HEX)
	local f_res4 = ProtoField.uint32("ls.res4","Reserved",base.HEX)
	local f_randkey = ProtoField.uint16("ls.randkey","Random Key",base.HEX)
	local f_seckeyindex = ProtoField.uint8("ls.randkey","secret Key index",base.HEX,nil,0xf0)
	local f_algver = ProtoField.uint8("ls.algver","Algrithm Version",base.HEX,nil,0x0f)
	local f_enlen = ProtoField.uint8("ls.enlen","Encrypted Length",base.DEC)
	local f_len = ProtoField.uint32("ls.len","Length",base.DEC)
	local f_type = ProtoField.uint16("ls.type","Type",base.HEX,{  [0x1001] = "login", [0x1f01] = "login response", [0x1002] = "heartbeat",[0x1f02] = "heartbeat response",[01003] = "push report",[0x1f03] = "push"})
	local f_pver = ProtoField.uint16("ls.pver","Protocol Version",base.HEX)
	local f_sid = ProtoField.uint16("ls.sid","Session ID",base.HEX)
	local f_chksum = ProtoField.uint16("ls.chksum","Checksum",base.HEX)
	local f_res1 = ProtoField.uint8("ls.res1","Reserved",base.HEX)

	local f_ext = ProtoField.bytes("ls.ext","ext",base.HEX)


	-- 前面定义的字段，需要通过p_heartbeat.fields注册才能在包详细信息面板中显示出来
	p_ls.fields = {f_randkey,f_seckeyindex,f_algver,f_enlen,f_res2,f_random,f_res1,f_res4,f_res3,f_len,f_type,f_pver,f_sid,f_loc,f_chksum,f_ext}


	local function loginv1_dissector1(buf,pinfo,t)
		local buf_len = buf:len()
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(3,1))
		t:add(f_len,buf(4,4))
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
		local rnum = buf_len - 16
		if rnum > 0 then
			t:add(f_ext,buf(16,rnum))
		end
    		pinfo.cols.info="Login Message"
	end


	local function loginrespv1_dissector1(buf,pinfo,t)
		local buf_len = buf:len()
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(3,1))
		t:add(f_len,buf(4,4))
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
		local rnum = buf_len - 16
		if rnum > 0 then
			t:add(f_ext,buf(16,rnum))
		end
    		pinfo.cols.info="Login V1 response Message"
	end

	local function htbtv1_dissector1(buf,pinfo,t)
		local buf_len = buf:len()
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(3,1))
		t:add(f_len,buf(4,4))
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
		local rnum = buf_len - 16
		if rnum > 0 then
			t:add(f_ext,buf(16,rnum))
		end
    		pinfo.cols.info="Heartbeat V1 Message"
	end

	local function htbtrespv1_dissector1(buf,pinfo,t)
	    local buf_len = buf:len()
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(3,1))
		t:add(f_len,buf(4,4))
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
		local rnum = buf_len - 16
		if rnum > 0 then
			t:add(f_ext,buf(16,rnum))
		end

    		pinfo.cols.info="Heartbeat V1 Response Message"
	end

	local function pushv1_dissector1(buf,pinfo,t)
	    local buf_len = buf:len()
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(3,1))
		t:add(f_len,buf(4,4))
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
		local rnum = buf_len - 16
		if rnum > 0 then
			t:add(f_ext,buf(16,rnum))
		end
    		pinfo.cols.info="PUSH V1 Message"
	end

	local function pushrespv1_dissector1(buf,pinfo,t)
		local buf_len = buf:len()
		t:add(f_randkey,buf(0,2))
		t:add(f_seckeyindex,buf(2,1))
		t:add(f_algver,buf(3,1))
		t:add(f_len,buf(4,4))
		t:add(f_type,buf(8,2))
		t:add(f_pver,buf(10,2))
		t:add(f_sid,buf(12,2))
		t:add(f_chksum,buf(14,2))
		local rnum = buf_len - 16
		if rnum > 0 then
			t:add(f_ext,buf(16,rnum))
		end

    		pinfo.cols.info="push V1 Response Message"
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
		secret_key={
		0xCC,  0x47,  0xE2,  0xE6,
      0x2D,  0x71,  0x74,  0x11,
      0x4D,  0x21,  0x28,  0xDD,
      0xD4,  0x6F,  0x21,  0x34,
      0xAc,  0x88,  0x0A,  0x75,
      0x55,  0x7F,  0x1A,  0xD4,
      0x9A,  0x46,  0x0A,  0x65,
      0xB4,  0x52,  0xC4,  0xC9,
      0x6C,  0x99,  0xBE,  0x68,
      0xCF,  0x77,  0x06,  0x60,
      0x1E,  0x63,  0x5F,  0x3C,
      0x89,  0xE1,  0x7F,  0x59,
      0x2E,  0x98,  0x0C,  0x65,
      0x1D,  0x36,  0x56,  0x58,
      0x71,  0xF9,  0xB6,  0x28,
      0x14,  0xA4,  0xCA,  0xA7,
      0x02,  0x83,  0x7A,  0x90,
      0x8D,  0x89,  0x8B,  0x13,
      0xC5,  0xD4,  0x13,  0xEC,
      0x20,  0xE1,  0xEE,  0xDA,
      0x98,  0x82,  0xD1,  0x4F,
      0xB2,  0x9c,  0x8D,  0xE4,
      0xD9,  0xC1,  0x97,  0xAF,
      0xCD,  0x8E,  0xF5,  0x87,
      0xAC,  0x17,  0x9B,  0x47,
      0xE0,  0x4E,  0xC6,  0xF1,
      0xE9,  0x7C,  0xA9,  0x95,
      0xF1,  0xF1,  0x97,  0xA2,
      0x1C,  0xEF,  0xA0,  0x6C,
      0x24,  0x8A,  0x0F,  0x7F,
      0xA6,  0x82,  0xF3,  0xC3,
      0x4D,  0x61,  0xDD,  0xC0
	                     }
            
		file = io.open("E:\\abc.txt", "w+")
		io.output(file)

		rand1 = buf(0,1):uint()
		rand2 = buf(1,1):uint()

		--io.write(rand1)
		--io.write("123")
		--io.write(rand2)
		for k=0,buf_len-1,1 do
			--io.write(string.format("%02X,",string.byte(buf[k]))
			--io.write(string.format("%02X,",buf[k]))
			io.write(string.format("%02X,",rand1))
			local randk = buf(k,1):uint()
			io.write(string.format("%02X,",randk))
			--io.write(rand1)
			io.write("\n")
		end

		io.write("------------------------------\n")

		local skeyb = bit.band(bit.rshift(buf(2,1):uint(),4),0x0f)

		io.write(string.format("%02X,",rand1))
		io.write(string.format("%02X,",rand2))
		io.write(string.format("%02X,",skeyb))
		io.write("\n")
		--io.write(string.format("%02X,%02X,%02X\n",skeyb,rand1,rand2))

		tkey = bit.bxor(rand2,rand1)
		
		skeyi = skeyb * 8
		
		local decmessage={}
		decmessage[1] = buf(0,1):uint()
		decmessage[2] = buf(1,1):uint()
		decmessage[3] = buf(2,1):uint()
		decmessage[4] = buf(3,1):uint()

		io.write(string.format("%02X,",decmessage[1]))
		io.write(string.format("%02X,",decmessage[2]))
		io.write(string.format("%02X,",decmessage[3]))
		io.write(string.format("%02X,",decmessage[4]))

		io.write("\nKLJDSLKFJDLFSKJLDKSJFLKSDJFLKJSDFLKDSFJ")

		
		for j=4,buf_len-1,1 do
			if skeyi > 127 then
				skeyi = 0
			end
			
			local t1 = bit.bxor(buf(j,1):uint(),tkey)
			local t2 = bit.bxor(t1,secret_key[skeyi+1])
			decmessage[j+1] = t2
			for k = 1,j+1,1 do
				io.write(string.format("%02X,",decmessage[k]))
			end
			io.write("\n")
			--io.write(string.format("%02X,",buf(j,1):uint()))
			--io.write(string.format("%02X,",tkey))
			--io.write(string.format("%02X,",skeyi))
			--io.write(string.format("%02X,",secret_key[skeyi+1]))
			--io.write(string.format("%02X,",t1))
			--io.write(string.format("%02X,",t2))
			--io.write("\n")
			
			--io.write("asdf")
			skeyi = skeyi + 1
			--decmessage[j] = bit.bxor(buf(j,1):uint(),key3)
			--decmessage[j+1] = bit.bxor(buf(j+1,1):uint(),key4)
			--io.write(buf[j])
			--io.write(buf[j+1])
		end

		

		--table.insert(decmessage,1,buf_len)

		io.write("++++++++++++++++++++++++++++++++\n")

		--解密数据转换成ByteArray类型
		local str = ''
		for i=1,buf_len do
			str = str .. string.format("%02x",decmessage[i])
			io.write(string.format("%02X,",decmessage[i]))
			io.write(str)
			io.write("\n")
		end
		
		io.write(str)
		io.write("\n")


		local b = ByteArray.new(str)
		
		io.close()

		local tvb = b:tvb("The Decrypted Data")
		local typ = tvb(8,2):uint()
		local len = tvb(4,4):uint()
		local ver = tvb(10,2):uint()
		local sub_t=t:add(tvb(),"The Decrypted Data")

		if len == buf_len and typ == 0x1001 then
		    t:append_text(": Login V1 Message")
		    loginv1_dissector1(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x1f01 then
		    t:append_text(": Login V1 Response Message")
		    loginrespv1_dissector1(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x1002 then
		    t:append_text(": Htbt V1 Response Message")
		    htbtv1_dissector1(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x1f02 then
		    t:append_text(": Htbt V1 Response Message")
		    htbtrespv1_dissector1(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x1003 then
		    t:append_text(": Push V1 Message")
		    pushrespv1_dissector1(tvb,pinfo,sub_t)
		elseif len == buf_len and typ == 0x1f03 then
		    t:append_text(": Puhs Response V1 Message")
		    pushv1_dissector1(tvb,pinfo,sub_t)

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
	      tcp_encap_table:add(8099,p_ls)
	      tcp_encap_table:add(8088,p_ls)
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

