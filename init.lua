-- static IP setup from http://www.domoticz.com/wiki/ESP8266_WiFi_module
print("Ready to start soft ap")
local str=wifi.ap.getmac();
local ssidTemp=string.format("%s%s%s",string.sub(str,10,11),string.sub(str,13,14),string.sub(str,16,17));

cfg={}
cfg.ssid="ESP8266_"..ssidTemp;
cfg.pwd="12345678"
wifi.ap.config(cfg)

cfg={}
cfg.ip="192.168.1.1";
cfg.netmask="255.255.255.0";
cfg.gateway="192.168.1.1";
wifi.ap.setip(cfg);
wifi.setmode(wifi.SOFTAP)

str=nil;
ssidTemp=nil;
collectgarbage();

print("Soft AP started")
print("Heep:(bytes)"..node.heap());
print("MAC:"..wifi.ap.getmac().."\r\nIP:"..wifi.ap.getip());
print("ESP8266 mode is: " .. wifi.getmode())
print("The module MAC address is: " .. wifi.ap.getmac())

pin = 4
status, temp, humi, temp_dec, humi_dec = dht.read(pin)
if status == dht.OK then
    print("DHT Temperature:"..temp..";".."Humidity:"..humi)
elseif status == dht.ERROR_CHECKSUM then
    print( "DHT Checksum error." )
elseif status == dht.ERROR_TIMEOUT then
    print( "DHT timed out." )
end

srv=net.createServer(net.TCP, 10)
print("Server created on " .. wifi.ap.getip())
srv:listen(80,function(conn)
    conn:on("receive",function(conn,request)
        print(request)
        
        pin = 2
        status, temp, humi, temp_dec, humi_dec = dht.read(pin)
        local t = temp;
        local h = humi;
        if status == dht.OK then
            print("DHT Temperature:"..temp..";".."Humidity:"..humi)
            conn:send("\"Temperature\": \""..temp.."\", \"Humidity\": \""..humi.."\"")
        elseif status == dht.ERROR_CHECKSUM then
            print( "DHT Checksum error." )
        elseif status == dht.ERROR_TIMEOUT then
            print( "DHT timed out." )
        end

        
    end)
    conn:on("sent",function(conn) conn:close() end)
end)
