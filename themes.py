#!/usr/bin/env python
# Author: Willie Lawrence
"""
'themes' has the default themes of lightk.
If you want create a new theme just follow these models
"""
LIGHT_BTN=[
	{
		"normal":{"fill":"#000","font":("TkDefaultFont",10)},
		"over":{"fill":"#000","font":("TkDefaultFont",10)},
		"clicked":{"fill":"#000","font":("TkDefaultFont",10)}
	},
	{
		"normal":{"fill":"#dadada","outline":"#dadada","width":1},
		"over":{"fill":"#ECECEC","outline":"#DADADA"},
		"clicked":{"fill":"#ECECEC","outline":"darkgray"}
	}
]
DARK_BTN=[
	{
		"normal":{"fill":"#fff","font":("TkDefaultFont",10)},
		"over":{"fill":"#fff","font":("TkDefaultFont",10)},
		"clicked":{"fill":"#fff","font":("TkDefaultFont",10)}
	},
	{
		"over":{"fill":"#444","width":0,"outline":"#444"},
		"normal":{"fill":"#333","width":0,"outline":"#333"},
		"clicked":{"fill":"#222","width":0,"outline":"#222"}
	}
]
YOUTUBE_BTN=[
	{
		"normal":{"fill":"#000","font":("TkDefaultFont",10)},
		"over":{"fill":"#000","font":("TkDefaultFont",10)},
		"clicked":{"fill":"#000","font":("TkDefaultFont",10)}
	},
	{
		"over":{"fill":"#F0F0F0","outline":"#CDCDCD"},
		"normal":{"fill":"#F8F8F8","outline":"#D4D4D4"},
		"clicked":{"fill":"#E9E9E9","outline":"#C7C7C7"}
	}
]
WINDOWS_8_BLUE_BTN=[
	{
		"normal":{"fill":"#fff", "font":("TkDefaultFont",10,"bold")},
		"over":{"fill":"#fff", "font":("TkDefaultFont",10,"bold")},
		"clicked":{"fill":"#fff", "font":("TkDefaultFont",10,"bold")}
	},
	{
		"over":{"fill":"#4FA3DF", "outline":"#B6D2EE"},
		"normal":{"fill":"#1A65B1", "width":2, "outline":"#B1CBE3"},
		"clicked":{"fill":"#53ACEC"}
	}
]
SUCCESS_BTN=[
	{
		"normal":{"fill":"#fff","font":("TkDefaultFont",10,"bold")},
		"over":{"fill":"#fff","font":("TkDefaultFont",10,"bold")},
		"clicked":{"fill":"#fff","font":("TkDefaultFont",10,"bold")}
	},
	{
		"normal":{"fill":"#649664","outline":"#DADADA","width":1},
		"over":{"fill":"#649664","outline":"#DADADA"},
		"clicked":{"fill":"#649664","outline":"darkgray"}
	}
]
WARN_BTN=[
	{
		"normal":{"fill":"#fff","font":("TkDefaultFont",10,"bold")},
		"over":{"fill":"#fff","font":("TkDefaultFont",10,"bold")},
		"clicked":{"fill":"#fff","font":("TkDefaultFont",10,"bold")}
	},
	{
		"normal":{"fill":"#BE6464","outline":"#DADADA","width":1},
		"over":{"fill":"#BE6464","outline":"#DADADA"},
		"clicked":{"fill":"#BE6464","outline":"darkgray"}
	}
]
GOOGLE_BLUE_BTN=[
	{"normal":{"fill":"#fff","font":("TkDefaultFont",10,"bold")},
		"over":{"fill":"#fff","font":("TkDefaultFont",10,"bold")},
		"clicked":{"fill":"#fff","font":("TkDefaultFont",10,"bold")}
	},
	{
		"normal":{"outline":"#3079ED","fill":"#4889F0","width":1},
		"over":{"outline":"#2F5BB7","fill":"#3C80EE"},
		"clicked":{"outline":"#274B99"}
	}
]
################################################################################
LIGHT_ENTRY = {
	"normal" : {
		"relief" : "flat", "highlightthickness" : 1,
		"highlightcolor" : "gray", "insertbackground":"darkgray",
		"bd" : 8, "insertwidth":1
	}
}
DARK_ENTRY = {
	"normal" : {
		"relief" : "flat", "highlightthickness" : 0,
		"highlightcolor" : "gray", "insertbackground":"darkgray",
		"bd" : 8, "insertwidth":1, "foreground":"#888",
		"background" : "#3a3a3a"
	},
	"over" : {
		"bg" : "#3b3b3b"
	}
}
GOOGLE_ENTRY = {
	"normal" : {
		"relief" : "flat", "highlightthickness" : 1,
		"highlightcolor" : "#4444dd", "insertbackground":"gray",
		"bd" : 8
	}
}

MODEL = [
	{}, # text first
	{} # than rectangle
	# the key must be: over, normal and clicked
]