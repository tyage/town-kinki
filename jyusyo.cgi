#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
#############################
# 役場の住所禄の外部閲覧。2007/11/13
#
############################
#unit.pl
#"住所" => "<form method=POST action=\"jyusyo.cgi\"><td height=32 width=32><input type=hidden name=mode value=\"jyusyo\"><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=k_id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><input type=image src='$img_dir/yakuba.gif' onMouseOver='onMes5(\"お店や会社を見ることが出来ます\")' onMouseOut='onMes5(\"\")'></td></form>\n",		#ver.1.40 2007/11/13

############################

$this_script = 'jyusyo.cgi';
require './town_ini.cgi';
require './town_lib.pl';
require './unit.pl';
&decode;

#メンテチェック
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
$seigenyou_now_time = time;
#制限時間チェック
		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}
		
#条件分岐
if($in{'mode'} eq "jyusyo"){&jyusyo;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;
#####################
sub jyusyo{
	$hausu_disp =1;#koko2007/12/14
	&header(yakuba_style);		#ver.1.30
	print <<"EOM";
	<table width="98%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>お店や会社を調べることが出来ます。<br>
<td  bgcolor=#00ff00 align=center width=35%><h2>住所案内</h2></td>
</tr></table><br>

EOM
		open(IN,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
		eval{ flock (IN, 1); };
		@ori_ie_para = <IN>;
		close(IN);
		@jyusyo=();
#koko2007/09/15
		$i=0;
		$nijyuu = 0;
	#	foreach (@ori_ie_para){
	#		if ($_ eq $ori_ie_para[0] && $i){
	#			$nijyuu = $i;
			#	&error("二重書き込み adm 1");
	#			last;
	#		}
	#		$i++;
	#	}
	#	if ($nijyuu){
	#		splice @ori_ie_para,$nijyuu;
	#		open(OUT,">$ori_ie_list") || &error("Open Error : $ori_ie_list");
	#		eval{ flock (OUT, 2); };
	#		print  OUT @ori_ie_para;
	#		close(IN);
	#	}
#kokoend
#koko2007/03/19
	#	open(OI,"< $ori_ie_list") || &error("Open Error : $ori_ie_list"); #koko2007/05/09
	#	@ori_ie_hairetu = <OI>;
		foreach (@ori_ie_para) { #foreach (@ori_ie_hairetu) {
			&ori_ie_sprit($_);
			$unit{"$ori_k_id"} = "<form method=POST action=\"original_house.cgi\"><input type=hidden name=mode value=houmon><input type=hidden name=ori_ie_id value=$ori_k_id><input type=hidden name=name value=\"$in{'name'}\"><input type=hidden name=pass value=\"$in{'pass'}\"><input type=hidden name=k_id value=\"$in{'k_id'}\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><input type=image src=\"$ori_ie_image\"><input type=hidden name=yakub value=\"in\"></form>\n";	#ver.1.40 #koko2006/12/13 #koko2007/04/27 #koko2007/09/17
		}
	#	close(OI);
#kokoend2007/03/19
		@tata=('A','B','C','D','E','F','G','H','I','J','K','L');

		foreach (@ori_ie_para){
			&ori_ie_sprit($_);
			$z=int(($ori_ie_tateziku-21)/16);
			$jyusyo[$ori_ie_town].="<TR><TD>$ori_ie_name</TD><TD>$unit{\"$ori_k_id\"}</TD><TD nowrap>$tata[$z]-$ori_ie_yokoziku<br>$ori_ie_syubetu</TD><TD>$ori_ie_setumei</TD></TR>\n"; #koko2007/03/17 #koko2007/03/19
		}
#個人の家情報をunitハッシュに代入
		print "<table border=\"1\" cellspacing=\"0\" cellpadding=\"5\" align=center class=yosumi bgcolor=#eeeecc><tr><TD ALIGN=left VALIGN=top width=100%>\n"; #koko2007/03/24

		$i = 0;
		foreach (@town_hairetu){ #town_ini.cgi にて設定されている。
			if($machikakushi eq 'yes'){#koko2007/10/21
				unless(($i == $kakushimachi_no && $kakushimachi_no) || ($i == $kakushimachi_no1 && $kakushimachi_no1) || ($i == $kakushimachi_no2 && $kakushimachi_no2) || ($i == $kakushimachi3_no && $kakushimachi_no3) || ($i == $kakushimachi_no4 && $kakushimachi_no4)){ #koko2007/06/13  3 = ダウンタウン
						print <<"EOM";
<!-- <table border="1" cellspacing="0" cellpadding="5" align=center class=yosumi bgcolor=#eeeecc><TD ALIGN=left VALIGN=top width=50%> -->
<table border="1" cellspacing="0" cellpadding="5" align=center class=yosumi bgcolor=#eeeecc width=100%><tr><td colspan=4>
$_
<BR>地価：$town_tika_hairetu[$i]万円
$jyusyo[$i]
</TD></tr></table>
EOM
				}
			}else{ #koko2007/10/22
				print <<"EOM";
<!-- <table border="1" cellspacing="0" cellpadding="5" align=center class=yosumi bgcolor=#eeeecc><TD ALIGN=left VALIGN=top width=50%> -->
<table border="1" cellspacing="0" cellpadding="5" align=center class=yosumi bgcolor=#eeeecc width=100%><tr><td colspan=4>
$_
<BR>地価：$town_tika_hairetu[$i]万円
$jyusyo[$i]
</TD></tr></table>
EOM
			}
		$i++;
		}
		print "</TD></tr></table>\n"; #koko2007/03/24

#	print "</table>";
	
	&hooter("login_view","戻る");
	exit;

}
