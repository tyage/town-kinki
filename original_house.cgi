#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
################　koko 2005/05/05
# 個人での１日のさい銭受け取り上限
$osaisenjyougen = 20000;
# トータルでの１日のさい銭受け取り上限
$totalosaisenjyougen = 100000;
# リンクのボタンを付ける('yes','no')
$linkbotan = 'no';
# 家を売却の時運営会社を消してしまう。 ('yes','no')
$baikyku_syoumetu = 'no';
# 二軒目以後の家の倍率 #koko2007/08/15
$ie_bairitu = 2;
################ kokoend

$this_script = 'original_house.cgi';
require './event.pl';
require './town_ini.cgi';
require './town_lib.pl';
require './unei_2.pl';
require './kaishiya.pl';
require './motimono_hanbai.pl';

&decode;
#メンテチェック
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
	
$seigenyou_now_time = time;
#制限時間チェック
		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}
		
#条件分岐
	if($in{'mode'} eq "my_house_settei"){&my_house_settei;}
	elsif($in{'mode'} eq "my_house_settei_do"){&my_house_settei_do;}
	elsif($in{'mode'} eq "houmon"){&houmon;}
	elsif($in{'mode'} eq "bbs1_settei_do"){&bbs1_settei_do;}
	elsif($in{'mode'} eq "omise_settei_do"){&omise_settei_do;}
	elsif($in{'mode'} eq "dokuzi_settei_do"){&dokuzi_settei_do;}
	elsif($in{'mode'} eq "gentei_settei_do"){&gentei_settei_do;}
	elsif($in{'mode'} eq "bbs_regist"){&bbs_regist;}
	elsif($in{'mode'} eq "gentei_delete"){&gentei_delete;}
	elsif($in{'mode'} eq "bbs_delete"){&bbs_delete;}
	elsif($in{'mode'} eq "gentei_regist"){&gentei_regist;}
	elsif($in{'mode'} eq "saisensuru"){&saisensuru;}
	elsif($in{'mode'} eq "comment_change"){&comment_change;}
	elsif($in{'mode'} eq "normal_bbs"){&normal_bbs;}
	elsif($in{'mode'} eq "house_change"){&house_change;}
	elsif($in{'mode'} eq "house_change2"){&house_change2;}
	elsif($in{'mode'} eq "my_syouhin"){&my_syouhin;}
	elsif($in{'mode'} eq "kaisya_bbs_do"){&kaisya_bbs_do;}
	elsif($in{'mode'} eq "seizou"){&seizou;}

	else{&error("「戻る」ボタンで街に戻ってください");}
exit;
	
#############以下サブルーチン

####自分の家の設定
sub my_house_settei {
	open(IN,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
	eval{ flock (IN, 1); };
	@ori_ie_para = <IN>;
	close(IN);
	$oriie_atta=0;
	$oriie_atta_my=0;
	foreach (@ori_ie_para){
		&ori_ie_sprit($_);
		if($in{'iesettei_id'} eq "$ori_k_id"){
			$oriie_atta_my=1;
			$oriie_atta=1;
			last;
		}
		if($in{'iesettei_id'}."_0" eq $ori_k_id or $in{'iesettei_id'}."_1" eq $ori_k_id or $in{'iesettei_id'}."_2" eq $ori_k_id or $in{'iesettei_id'}."_3" eq $ori_k_id){
			$oriie_atta=1;
		}
	}
	if ($oriie_atta == 0){&error("家が見つかりません。");}
	
	#家設定ファイルがなければ作成
	$my_directry = "./member/$in{'iesettei_id'}";
	$oriie_settei_file="$my_directry/oriie_settei.cgi";
	if (! -e $oriie_settei_file){
		open(OIS,">$oriie_settei_file") || &error("Write Error : $oriie_settei_file");
		eval{ flock (OIS, 2); };
		chmod 0666,"$oriie_settei_file";
		close(OIS);
	}
	open(OIS,"< $oriie_settei_file") || &error("Open Error : $oriie_settei_file");
	eval{ flock (OIS, 1); };
	$kihon_oriie_settei = <OIS>;
	&oriie_settei_sprit ($kihon_oriie_settei);
	close(OIS);
	
	#ヘッダー
	&header(kentiku_style);
	if ($in{'iesettei_id'} eq "$k_id"){$settei_title = "自分の家設定"; $settei_t_color = "#336699";}
	else{$settei_title = "配偶者の家設定"; $settei_t_color = "#ff6666";}
	
	print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
<tr bgcolor=$settei_t_color><td align=center style="color:#ffffff;font-size:13px;">$settei_title</td></tr></table><br>
EOM
	
	#自分の家があるとき
	if($oriie_atta_my){
		#それぞれ表示
		if ($my_con1 eq "0"){&bbs1_settei;}elsif ($my_con1 eq "1"){&omise_settei;}elsif ($my_con1 eq "2"){&dokuzi_settei;}elsif ($my_con1 eq "3"){&gentei_settei;}
		if ($my_con2 eq "0"){&bbs1_settei;}elsif ($my_con2 eq "1"){&omise_settei;}elsif ($my_con2 eq "2"){&dokuzi_settei;}elsif ($my_con2 eq "3"){&gentei_settei;}	
		if ($my_con3 eq "0"){&bbs1_settei;}elsif ($my_con3 eq "1"){&omise_settei;}elsif ($my_con3 eq "2"){&dokuzi_settei;}elsif ($my_con3 eq "3"){&gentei_settei;}	
		if ($my_con4 eq "0"){&bbs1_settei;}elsif ($my_con4 eq "1"){&omise_settei;}elsif ($my_con4 eq "2"){&dokuzi_settei;}elsif ($my_con4 eq "3"){&gentei_settei;}
		
		#店を持っていない時
		if(!($my_con1 eq "1" || $my_con2 eq "1" || $my_con3 eq "1" || $my_con4 eq "1")){
			@new_ori_ie_list1 = ();
			foreach (@ori_ie_para){
				&ori_ie_sprit($_);
				if ($in{'iesettei_id'} eq $ori_k_id){
					$ori_ie_syubetu = '店無し';
				}
				&ori_ie_temp;
				push (@new_ori_ie_list1,$ori_ie_temp);
			}
			
			#家リスト更新
			$i=0;
			$nijyuu = 0;
			foreach (@new_ori_ie_list1){
				if ($_ eq $new_ori_ie_list1[0] && $i){
					$nijyuu = $i;
					&error("二重書き込み o_h 1");
					last;
				}
				$i++;
			}
			if ($nijyuu){
				splice @new_ori_ie_list1,$nijyuu;
			}
			
			open(OIO,">$ori_ie_list") || &error("$ori_ie_listに書き込めません");
			eval{ flock (OIO, 2); };
			print OIO @new_ori_ie_list1;
			close(OIO);
		}
	    
		foreach (@ori_ie_para){
			&ori_ie_sprit($_);
			if ($in{'iesettei_id'} eq "$ori_k_id"){last;}
		}
	    
		print <<"EOM";
<br>
<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
<tr><td>
<div class=tyuu>■基本設定</div>
<form method="POST" action="$this_script">
<input type=hidden name=mode value="my_house_settei_do">
<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
●コンテンツ選択（※設置するコンテンツを選択してください。後で変更も可能\です。ここのタイトルはページ上のボタンに表\示させるものです）<br>
EOM
		
		if ($ori_ie_rank2 != 3){print "ここで一番上にあるコンテンツが家に入ったとき最初に表\示されます。<br>";}
	
		if ($ori_ie_rank2 == 0){$ii=4;}elsif($ori_ie_rank2 == 1){$ii=3;}elsif($ori_ie_rank2 == 2){$ii=2;}elsif($ori_ie_rank2 == 3){$ii=1;}
		
		$selectcount = 0;
		$titlecount = 4;
		foreach (1..$ii){
			if ($ori_ie_rank2 != 3){print "<div class=honbun2>○$_つめのコンテンツ</div>";}
			print <<"EOM";
<select name="my_con$_">
<option value="">公開しない</option>
EOM
			print "<option value=0";
			if ($oriie_settei_sprit[$selectcount] eq "0"){print " selected";}
			print ">通常の掲示板</option>\n";
			print "<option value=1";
			if ($oriie_settei_sprit[$selectcount] eq "1"){print " selected";}
			print ">お店</option>\n";
			print "<option value=2";
			if ($oriie_settei_sprit[$selectcount] eq "2"){print " selected";}
			print ">独自URL</option>\n";
			print "<option value=3";
			if ($oriie_settei_sprit[$selectcount] eq "3"){print " selected";}
			print ">家主のみ書ける掲示板</option>\n";
			print "</select>\n";
	
			if ($ori_ie_rank != 3) {print "タイトル <input type=text name=\"title$_\" value=\"$oriie_settei_sprit[$titlecount]\">";}
				$selectcount ++;
				$titlecount ++;
		}
		print "<input type=submit value=OK></form><hr size=1>";
	}else{
		print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
<tr><td>
<div class=tyuu>■基本設定</div>
<br>
EOM
	}
	
	print "●街で家にマウスがのった時に表\示されるコメント（40字以内）<br>";
	
	foreach (@ori_ie_para){
		&ori_ie_sprit($_);
		if ("$in{'iesettei_id'}" eq $ori_k_id){
		     $cha_ie.="<option value=\"\">普通の家を</option>\n";
		}
		if ("$in{'iesettei_id'}"."_0" eq $ori_k_id){
		     $cha_ie.="<option value=\"_0\">支店を</option>\n";
		}
		if ("$in{'iesettei_id'}"."_1" eq $ori_k_id){
		     $cha_ie.="<option value=\"_1\">運営会社を</option>\n";
		}
		if ("$in{'iesettei_id'}"."_2" eq $ori_k_id){
		     $cha_ie.="<option value=\"_2\">株式会社を</option>\n";
		}
		if ("$in{'iesettei_id'}"."_3" eq $ori_k_id){
		     $cha_ie.="<option value=\"_3\">持ち物販売店を</option>\n";
		}
	}
    
	$dispin = "";
	$my_iesettei_id = $in{'iesettei_id'};
	foreach (@ori_ie_para){
		&ori_ie_sprit($_);
		($my_iesettei_id,$bangou) = split(/_/,$my_iesettei_id);
		($ori_k_id2,$bangou2) = split(/_/,$ori_k_id);
		if ($my_iesettei_id eq "$ori_k_id2"){
			print <<"EOM";
<form method="POST" action="$this_script" style="margin-top:0;margin-bottom:0;">
<input type=hidden name=mode value="comment_change">
<input type=hidden name=iesettei_id value="$ori_k_id">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=text name=ori_ie_setumei size=80 value=$ori_ie_setumei>
<input type=submit value="OK">
</form>
EOM
		}
	}
	
	print <<"EOM";
<hr size=1>
●建物の外観、内装（コンテンツ内容）の変更<br>
場所はそのままに、家の外観を変更したり、内装をアップグレードすることができます。<br>
<form method="POST" action="$this_script">
<input type=hidden name=mode value="house_change">
<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<select name="iesuu">
$cha_ie
</select>
<input type=submit value=" 変更する "></form>
<hr size=1>
EOM

	if ($in{'iesettei_id'} eq "$k_id"){
		foreach (@ori_ie_para){
			&ori_ie_sprit($_);
			if ("$in{'iesettei_id'}" eq $ori_k_id){
			     $uru_ie.="<option value=\"\">普通の家を</option>\n";
			}
			if ("$in{'iesettei_id'}"."_0" eq $ori_k_id){
			     $uru_ie.="<option value=\"_0\">支店を</option>\n";
			}
			if ("$in{'iesettei_id'}"."_1" eq $ori_k_id){
			     $uru_ie.="<option value=\"_1\">運営会社を</option>\n";
			}
			if ("$in{'iesettei_id'}"."_2" eq $ori_k_id){
			     $uru_ie.="<option value=\"_2\">株式会社を</option>\n";
			}
			if ("$in{'iesettei_id'}"."_3" eq $ori_k_id){
			     $uru_ie.="<option value=\"_3\">持ち物販売店を</option>\n";
			}
		}
		print <<"EOM";
●建物の売却<br>
家の場所を変更したい場合は、一度家を売却してから再度購入してくだい。<br>
売却で得られるのは土地の価格だけです。<br>
現在のコンテンツ内容は新たに家を購入した場合も保持されています。<br>
<form method="POST" action="$this_script">
<input type=hidden name=mode value="house_change">
<input type=hidden name=command value="baikyaku">
<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<select name="iesuu">
$uru_ie
</select>
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value=" 売却する "></form>	
EOM

	}else{
		print "※配偶者の家の場合、売却処理はできません。";
	}
	
	print "<div align=center><a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div></td></tr></table>";
	&hooter("login_view","戻る");
	
	exit;
}

###コメント変更
sub comment_change {
	if (length($in{'ori_ie_setumei'}) > 80) {&error("コメントは40字以内です");}
	if ($in{'ori_ie_setumei'} =~ /'/) {&error("半角の「'」は使用できません。");}		#ver.1.3
	&lock;
	open(IN,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
	eval{ flock (IN, 1); };
	@ori_ie_para = <IN>;
	close(IN);
	@new_ori_ie_para2 = (); #koko2007/07/11
	foreach (@ori_ie_para){
		&ori_ie_sprit($_);
		if ($in{'iesettei_id'} eq $ori_k_id){
			$ori_ie_setumei = $in{'ori_ie_setumei'};
		}
		&ori_ie_temp;
		push (@new_ori_ie_para2,$ori_ie_temp);#koko2007/03/23
	}

#koko2007/09/15
		$i=0;
		$nijyuu = 0;
		foreach (@new_ori_ie_para2){
			if ($_ eq $new_ori_ie_para2[0] && $i){
				$nijyuu = $i;
				&error("二重書き込み o_h 2");
				last;
			}
			$i++;
		}
		if ($nijyuu){
			splice @new_ori_ie_para2,$nijyuu;
		}
#kokoend

	open(OLOUT,">$ori_ie_list") || &error("$ori_ie_listに書き込みが出来ません");
	eval{ flock (OLOUT, 2); };
	print OLOUT @new_ori_ie_para2;#koko2007/03/23
	close(OLOUT);
	&unlock;
	&message("家のコメントを変更しました。","my_house_settei","original_house.cgi");
}


###自分の家の設定処理
sub my_house_settei_do {
	$my_directry = "./member/$in{'iesettei_id'}";
	$oriie_settei_file="$my_directry/oriie_settei.cgi";
		open(OIS,"< $oriie_settei_file") || &error("Open Error : $oriie_settei_file");
		eval{ flock (OIS, 1); };
		$kihon_oriie_settei = <OIS>;
		&oriie_settei_sprit ($kihon_oriie_settei);
		close(OIS);
		
		$my_con1 = $in{'my_con1'};
		$my_con2 = $in{'my_con2'};
		$my_con3 = $in{'my_con3'};
		$my_con4 = $in{'my_con4'};
		$my_con1_title = $in{'title1'};
		$my_con2_title = $in{'title2'};
		$my_con3_title = $in{'title3'};
		$my_con4_title = $in{'title4'};
		$my_yobi5 = $in{'my_yobi5'};
		$my_yobi6 = $in{'my_yobi6'};
		$my_yobi7 = $in{'my_yobi7'};
		&oriie_settei_temp;
	&lock;
	open(OLOUT,">$oriie_settei_file") || &error("$oriie_settei_fileに書き込みが出来ません");
	eval{ flock (OLOUT, 2); };
	print OLOUT $ori_ie_settei_temp;
	close(OLOUT);
	&unlock;
	&my_house_settei;
}

####BBS1の設定
sub bbs1_settei {
#管理者作成BBSの場合
	if ($in{'mode'} eq "admin_bbs"){
			$my_directry = "./member/admin";
			if (! -d $my_directry){
				mkdir($my_directry, 0755) || &error("Error : can not Make Directry");
				if ($zidouseisei == 1){
					chmod 0777,"$my_directry";
				}elsif ($zidouseisei == 2){
					chmod 0755,"$my_directry";
				}else{
					chmod 0755,"$my_directry";
				}
			}
			$bbs1_settei_file="$my_directry/bbs".$in{'bbs_num'}."_ini.cgi";
			if (! -e $bbs1_settei_file){
				open(OIB,">$bbs1_settei_file") || &error("Write Error : $bbs1_settei_file");
				eval{ flock (OIB, 2); };
				chmod 0666,"$bbs1_settei_file";
				close(OIB);
			}
			$bbs1_log_file="$my_directry/bbs".$in{'bbs_num'}."_log.cgi";
			if (! -e $bbs1_log_file){
				open(OIL,">$bbs1_log_file") || &error("Write Error : $bbs1_log_file");
				eval{ flock (OIL, 2); };
				chmod 0666,"$bbs1_log_file";
				close(OIL);
			}
	}else{
			$my_directry = "./member/$in{'iesettei_id'}";
			$bbs1_settei_file="$my_directry/bbs1_ini.cgi";
			if (! -e $bbs1_settei_file){
				open(OIB,">$bbs1_settei_file") || &error("Write Error : $bbs1_settei_file");
				eval{ flock (OIB, 2); };
				chmod 0666,"$bbs1_settei_file";
				close(OIB);
			}
			$bbs1_log_file="$my_directry/bbs1_log.cgi";
			if (! -e $bbs1_log_file){
				open(OIL,">$bbs1_log_file") || &error("Write Error : $bbs1_log_file");
				eval{ flock (OIL, 2); };
				chmod 0666,"$bbs1_log_file";
				close(OIL);
			}
	}
		open(OIB,"< $bbs1_settei_file") || &error("Open Error : $bbs1_settei_file");
		eval{ flock (OIB, 1); };
			$bbs1_settei_data = <OIB>;
			($bbs1_title,$bbs1_come,$bbs1_body_style,$bbs1_toukousya_style,$bbs1_table2_style,$bbs1_toukouwidth,$bbs1_a_hover_style,$bbs1_tablewidth,$bbs1_title_style,$bbs1_leed_style,$bbs1_siasenbako,$bbs1_yobi5,$bbs1_yobi6,$bbs1_yobi7,$bbs1_yobi8,$bbs1_yobi9,$bbs1_yobi10,$bbs_link)= split(/<>/,$bbs1_settei_data); #koko2007/06/26
	chomp $bbs_link; #koko2007/06/26
#bbs1_yobi5 = 記事番号のスタイル　bbs1_yobi6＝同じ街の住民専用掲示板　bbs1_yobi7＝inputのスタイル
		close(OIB);
		
#スタイルの初期化
	if ($bbs1_body_style eq ""){$bbs1_body_style = "background-color:#ffcc66;";$syokika = 1;} #koko2007/03/21
	if ($bbs1_title_style eq ""){$bbs1_title_style = "font-size: 16px; color: #666666;line-height:180%; text-align:center;";}
	if ($bbs1_leed_style eq ""){$bbs1_leed_style = "font-size: 11px; line-height: 16px; color: #336699";}
	if ($bbs1_yobi5 eq ""){$bbs1_yobi5 = "font-size: 15px; color: #336699";}
	if ($bbs1_toukousya_style eq ""){$bbs1_toukousya_style = "font-size: 11px; color: #000000";}
	if ($bbs1_table2_style eq ""){$bbs1_table2_style = "font-size: 11px; line-height: 16px; color: #666666; background-color:#ffffcc; border: #336699; border-style: dotted; border-width:4px";}
	if ($bbs1_toukouwidth eq ""){$bbs1_toukouwidth = "50";}
	if ($bbs1_a_hover_style eq ""){$bbs1_a_hover_style = " color:#333333;text-decoration: none";}
	if ($bbs1_tablewidth eq ""){$bbs1_tablewidth = "500";}
	if ($bbs1_siasenbako eq ""){$bbs1_siasenbako = "font-size:11px;color:#000000";}
	if ($bbs1_yobi7 eq ""){$bbs1_yobi7 = "font-size:11px;color:#000000";}

	if ($bbs_link){$bbs_link_check = " checked";}

	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="bbs1_settei_do">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=admin_pass value="$in{'admin_pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
EOM
	if ($in{'mode'} eq "admin_bbs"){
	print "<input type=hidden name=bbs_num value=\"$in{'bbs_num'}\">\n";
	print "<input type=hidden name=command value=\"admin_bbs\">\n";
	}
	print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
	<tr><td>
EOM
	if ($in{'mode'} eq "admin_bbs"){
		print "<div class=tyuu>■$admin_bbs_syurui[$in{'bbs_num'}]の掲示板設定</div>";
	}else{
		print "<div class=tyuu>■通常の掲示板設定</div>";
	}
	print <<"EOM";
	●掲示板のタイトル（タグ指定可。絶対URLならばイメージ画像の指定も可）<br>
	<textarea  cols=80 rows=4 name="title" wrap="soft">$bbs1_title</textarea><br>
	●タイトル下のコメント<br>
	<textarea  cols=80 rows=3 name="comento" wrap="soft">$bbs1_come</textarea><br>
	●背景のスタイル設定<br>
	<input type=text name="bbs1_body_style" size=120 value="$bbs1_body_style"><br>
	●タイトルのスタイル設定<br>
	<input type=text name="bbs1_title_style" size=120 value="$bbs1_title_style"><br>
	●タイトル下のコメントのスタイル設定<br>
	<input type=text name="bbs1_leed_style" size=120 value="$bbs1_leed_style"><br>
	●記事番号のスタイル設定<br>
	<input type=text name="bbs1_yobi5" size=120 value="$bbs1_yobi5"><br>
	●投稿者名のスタイル設定<br>
	<input type=text name="bbs1_toukousya_style" size=120 value="$bbs1_toukousya_style"><br>
	●掲示板内の基本スタイル設定<br>
	<input type=text name="bbs1_table2_style" size=120 value="$bbs1_table2_style"><br>
	●投稿欄のサイズ（半角文字数で指定）<br>
	<input type=text name="bbs1_toukouwidth" size=120 value="$bbs1_toukouwidth"><br>
	●リンク（aタグ）のスタイル設定<br>
	<input type=text name="bbs1_a_hover_style" size=120 value="$bbs1_a_hover_style"><br>
	●テーブルの横幅<br>
	<input type=text name="bbs1_tablewidth" size=120 value="$bbs1_tablewidth"><br>
	●inputとselectのスタイル設定<br>
	<input type=text name="bbs1_siasenbako" size=120 value="$bbs1_siasenbako"><br>
	●レス部分のスタイル設定<br>
	<input type=text name="bbs1_yobi7" size=120 value="$bbs1_yobi7"><br>
	●掲示板書き込みでリンクボタンを使う<br><!-- koko2007/06/26 -->
	<input type=checkbox name="bbs_link" value="1"$bbs_link_check>掲示板のリンクを使う<br>
EOM
	if ($in{'mode'} eq "admin_bbs"){
		print <<"EOM";
	●同じ街の住民専用掲示板にする（この掲示板を設置した街に住んでいる人だけが閲覧・書き込みできます）<br>
	<select name="bbs1_yobi6">
	<option value="">通常</option>
EOM
	if ($bbs1_yobi6 eq "on"){
		print "<option value=\"on\" selected>同じ街の住民専用</option>";
	}else{
		print "<option value=\"on\">同じ街の住民専用</option>"
	}
	print "</select><br><br>";
	}
	
	print "<input type=submit value=設定変更>";

		if ($in{'mode'} eq "admin_bbs"){
		print <<"EOM";
	<a href="$this_script?mode=normal_bbs&ori_ie_id=admin&bbs_num=$in{'bbs_num'}&name=$in{'name'}&admin_pass=$in{'admin_pass'}&con_sele=0" target=_blank>[現在の設定内容の確認]</a>
	</td></tr></table>
	</form>
EOM
		}else{
		print <<"EOM";
	<a href="$this_script?mode=houmon&ori_ie_id=$in{'iesettei_id'}&name=$in{'name'}&pass=$in{'pass'}&con_sele=0" target=_blank>[現在の設定内容の確認]</a>
	</td></tr></table>
	</form>
EOM
		}
#koko2007/03/21
	if ($syokika){
		chomp $bbs_link; #koko2007/06/26
		$bbs_settei_temp = "$bbs1_title<>$bbs1_come<>$bbs1_body_style<>$bbs1_toukousya_style<>$bbs1_table2_style<>$bbs1_toukouwidth<>$bbs1_a_hover_style<>$bbs1_tablewidth<>$bbs1_title_style<>$bbs1_leed_style<>$bbs1_siasenbako<>$bbs1_yobi5<>$bbs1_yobi6<>$bbs1_yobi7<>$bbs1_yobi8<>$bbs1_yobi9<>$bbs1_yobi10<>$bbs_link<>\n"; #koko2007/06/26
		open(OLOUT,">$bbs1_settei_file") || &error("$bbs1_settei_fileに書き込みが出来ません");
		eval{ flock (OLOUT, 2); };
		print OLOUT $bbs_settei_temp;
		close(OLOUT);
	}
#kokoend2007/03/21
}

sub bbs1_settei_do {
#管理者作成BBSの場合
	if ($in{'command'} eq "admin_bbs"){
		$bbs1_settei_file="./member/admin/bbs".$in{'bbs_num'}."_ini.cgi";
	}else{
		$bbs1_settei_file="./member/$in{'iesettei_id'}/bbs1_ini.cgi";
	}
		open(OIB,"< $bbs1_settei_file") || &error("Open Error : $bbs1_settei_file");
		eval{ flock (OIB, 1); };
			$bbs1_settei_data = <OIB>;
			($bbs1_title,$bbs1_come,$bbs1_body_style,$bbs1_toukousya_style,$bbs1_table2_style,$bbs1_toukouwidth,$bbs1_a_hover_style,$bbs1_tablewidth,$bbs1_title_style,$bbs1_leed_style,$bbs1_siasenbako,$bbs1_yobi5,$bbs1_yobi6,$bbs1_yobi7,$bbs1_yobi8,$bbs1_yobi9,$bbs1_yobi10,$bbs_link)= split(/<>/,$bbs1_settei_data); #koko2007/06/26
		close(OIB);
		chomp $bbs_link; #koko2007/06/26
		&lock;
	        $bbs1_title = $in{'title'};#koko2008/04/04
	        $bbs1_come = $in{'comento'};#koko2008/04/04
			$bbs1_body_style = $in{'bbs1_body_style'};
			$bbs1_toukousya_style = $in{'bbs1_toukousya_style'};
			$bbs1_table2_style = $in{'bbs1_table2_style'};
			$bbs1_toukouwidth = $in{'bbs1_toukouwidth'};
			$bbs1_a_hover_style = $in{'bbs1_a_hover_style'};
			$bbs1_tablewidth = $in{'bbs1_tablewidth'};
			$bbs1_title_style = $in{'bbs1_title_style'};
			$bbs1_leed_style = $in{'bbs1_leed_style'};
			$bbs1_siasenbako = $in{'bbs1_siasenbako'};
			$bbs1_yobi5 = $in{'bbs1_yobi5'};
			$bbs1_yobi6 = $in{'bbs1_yobi6'};
			$bbs1_yobi7 = $in{'bbs1_yobi7'};
			$bbs1_yobi8 = $in{'bbs1_yobi8'};
			$bbs1_yobi9 = $in{'bbs1_yobi9'};
			$bbs1_yobi10 = $in{'bbs1_yobi10'};

			$bbs_link = $in{'bbs_link'}; #koko2007/06/26

		$bbs_settei_temp = "$bbs1_title<>$bbs1_come<>$bbs1_body_style<>$bbs1_toukousya_style<>$bbs1_table2_style<>$bbs1_toukouwidth<>$bbs1_a_hover_style<>$bbs1_tablewidth<>$bbs1_title_style<>$bbs1_leed_style<>$bbs1_siasenbako<>$bbs1_yobi5<>$bbs1_yobi6<>$bbs1_yobi7<>$bbs1_yobi8<>$bbs1_yobi9<>$bbs1_yobi10<>$bbs_link<>\n"; #koko2007/06/26
	open(OLOUT,">$bbs1_settei_file") || &error("$bbs1_settei_fileに書き込みが出来ません");
	eval{ flock (OLOUT, 2); };
	print OLOUT $bbs_settei_temp;
	close(OLOUT);
		&unlock;
		if ($in{'command'} eq "admin_bbs"){
			&header;
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>設定を変更しました。</td></tr></table><br>
	
	<form method=POST action="$script">
	<input type=hidden name=mode value="admin_bbs">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=admin_pass value="$in{'admin_pass'}">
	<input type=hidden name=bbs_num value="$in{'bbs_num'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="戻る">
	</form></div>
EOM
	exit;
		}else{
			&my_house_settei;
		}
}

####家主掲示板の設定
sub gentei_settei {
	$my_directry = "./member/$in{'iesettei_id'}";
	$gentei_settei_file="$my_directry/gentei_ini.cgi";
	if (! -e $gentei_settei_file){
		open(OIB,">$gentei_settei_file") || &error("Write Error : $gentei_settei_file");
		eval{ flock (OIB, 2); };
		chmod 0666,"$gentei_settei_file";
		close(OIB);
	}
	$gentei_log_file="$my_directry/gentei_log.cgi";
	if (! -e $gentei_log_file){
		open(OIL,">$gentei_log_file") || &error("Write Error : $gentei_log_file");
		eval{ flock (OIL, 2); };
		chmod 0666,"$gentei_log_file";
		close(OIL);
	}
		open(OIB,"< $gentei_settei_file") || &error("Open Error : $gentei_settei_file");
		eval{ flock (OIB, 1); };
			$gentei_settei_data = <OIB>;
			($gentei_title,$gentei_come,$gentei_body_style,$gentei_daimei_style,$gentei_table2_style,$gentei_kensuu,$gentei_tablewidth,$gentei_title_style,$gentei_leed_style,$gentei_siasenbako,$gentei_yobi5,$gentei_yobi6,$gentei_yobi7,$gentei_yobi8,$gentei_yobi9,$gentei_yobi10)= split(/<>/,$gentei_settei_data);
		close(OIB);
		
#スタイルの初期化
	if ($gentei_body_style eq ""){$gentei_body_style = "background-color:#99cc99;";$syokika = 1;} #koko2007/03/21
	if ($gentei_title_style eq ""){$gentei_title_style = "font-size: 20px; color: #339966;line-height:150%; text-align:center;";}
	if ($gentei_leed_style eq ""){$gentei_leed_style = "font-size: 11px; color: #ff6600;line-height:160%;";}
	if ($gentei_daimei_style eq ""){$gentei_daimei_style = "font-size: 14px; color: #445555;line-height:200%;";}
	if ($gentei_table2_style eq ""){$gentei_table2_style = "font-size: 11px; line-height: 16px; color: #666666; background-color:#ffffcc; border: #339966; border-style: dotted; border-width:4px;";}
	if ($gentei_kensuu eq ""){$gentei_kensuu = "5";}
	if ($gentei_tablewidth eq ""){$gentei_tablewidth = "520";}
	if ($gentei_siasenbako eq ""){$gentei_siasenbako = "font-size:11px;color:#000000";}
	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="gentei_settei_do">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
	<tr><td>
	<div class=tyuu>■家主掲示板の設定</div>
	●掲示板のタイトル（タグ指定可。絶対URLならばイメージ画像の指定も可）<br>
	<textarea  cols=80 rows=4 name="title" wrap="soft">$gentei_title</textarea><br>
	●タイトル下のコメント<br>
	<textarea  cols=80 rows=3 name="comento" wrap="soft">$gentei_come</textarea><br>
	●背景のスタイル設定<br>
	<input type=text name="gentei_body_style" size=120 value="$gentei_body_style"><br>
	●掲示板タイトルのスタイル設定<br>
	<input type=text name="gentei_title_style" size=120 value="$gentei_title_style"><br>
	●タイトル下のコメントのスタイル設定<br>
	<input type=text name="gentei_leed_style" size=120 value="$gentei_leed_style"><br>
	●記事の題名のスタイル設定<br>
	<input type=text name="gentei_daimei_style" size=120 value="$gentei_daimei_style"><br>
	●掲示板内の基本スタイル設定<br>
	<input type=text name="gentei_table2_style" size=120 value="$gentei_table2_style"><br>
	●１ページに表\示する記事件数（半角文字数で指定）<br>
	<input type=text name="gentei_kensuu" size=120 value="$gentei_kensuu"><br>
	●テーブルの横幅<br>
	<input type=text name="gentei_tablewidth" size=120 value="$gentei_tablewidth"><br>
	●inputとselectのスタイル設定<br>
	<input type=text name="gentei_siasenbako" size=120 value="$gentei_siasenbako"><br>
	<input type=submit value=設定変更>
	<a href="$this_script?mode=houmon&ori_ie_id=$in{'iesettei_id'}&name=$in{'name'}&pass=$in{'pass'}&con_sele=3" target=_blank>[現在の設定内容の確認]</a>
	</form>
	
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="gentei_regist">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=ori_ie_id value="$k_id">
	<input type=hidden name=town_no value="$in{'town_no'}"><br><br>
	<div class=tyuu>■投稿（タグ可）</div>
	タイトル<br>
	<input type=text name="b_title" size=80><br>
	内容<br>
	<textarea  cols=90 rows=7 name="b_come" wrap="soft"></textarea><br>
	<input type=submit value="投稿">
	</form>
	</td></tr></table>
	
EOM
#koko2007/03/21
	if ($syokika){
		$gentei_settei_temp = "$gentei_title<>$gentei_come<>$gentei_body_style<>$gentei_daimei_style<>$gentei_table2_style<>$gentei_kensuu<>$gentei_tablewidth<>$gentei_title_style<>$gentei_leed_style<>$gentei_siasenbako<>$gentei_yobi5<>$gentei_yobi6<>$gentei_yobi7<>$gentei_yobi8<>$gentei_yobi9<>$gentei_yobi10<>\n";
		open(OLOUT,">$gentei_settei_file") || &error("$gentei_settei_fileに書き込みが出来ません");
		eval{ flock (OLOUT, 2); };
		print OLOUT $gentei_settei_temp;
		close(OLOUT);
	}
#kokoend
}

sub gentei_settei_do {
	$gentei_settei_file="./member/$in{'iesettei_id'}/gentei_ini.cgi";
		open(OIB,"< $gentei_settei_file") || &error("Open Error : $gentei_settei_file");
		eval{ flock (OIB, 1); };
			$gentei_settei_data = <OIB>;
			($gentei_title,$gentei_come,$gentei_body_style,$gentei_daimei_style,$gentei_table2_style,$gentei_kensuu,$gentei_tablewidth,$gentei_title_style,$gentei_leed_style,$gentei_siasenbako,$gentei_yobi5,$gentei_yobi6,$gentei_yobi7,$gentei_yobi8,$gentei_yobi9,$gentei_yobi10)= split(/<>/,$gentei_settei_data);
		close(OIB);
		
		&lock;
	        $gentei_title = $in{'title'};#koko2008/04/04
	        $gentei_come = $in{'comento'};#koko2008/04/04
			$gentei_body_style = $in{'gentei_body_style'};
			$gentei_daimei_style = $in{'gentei_daimei_style'};
			$gentei_table2_style = $in{'gentei_table2_style'};
			$gentei_kensuu = $in{'gentei_kensuu'};
			$gentei_tablewidth = $in{'gentei_tablewidth'};
			$gentei_title_style = $in{'gentei_title_style'};
			$gentei_leed_style = $in{'gentei_leed_style'};
			$gentei_siasenbako = $in{'gentei_siasenbako'};
			$gentei_yobi5 = $in{'gentei_yobi5'};
			$gentei_yobi6 = $in{'gentei_yobi6'};
			$gentei_yobi7 = $in{'gentei_yobi7'};
			$gentei_yobi8 = $in{'gentei_yobi8'};
			$gentei_yobi9 = $in{'gentei_yobi9'};
			$gentei_yobi10 = $in{'gentei_yobi10'};
		$gentei_settei_temp = "$gentei_title<>$gentei_come<>$gentei_body_style<>$gentei_daimei_style<>$gentei_table2_style<>$gentei_kensuu<>$gentei_tablewidth<>$gentei_title_style<>$gentei_leed_style<>$gentei_siasenbako<>$gentei_yobi5<>$gentei_yobi6<>$gentei_yobi7<>$gentei_yobi8<>$gentei_yobi9<>$gentei_yobi10<>\n";
	open(OLOUT,">$gentei_settei_file") || &error("$gentei_settei_fileに書き込みが出来ません");
	eval{ flock (OLOUT, 2); };
	print OLOUT $gentei_settei_temp;
	close(OLOUT);
		&unlock;
		&my_house_settei;
}


####お店の設定
sub omise_settei {
	$my_directry = "./member/$in{'iesettei_id'}";
	$omise_settei_file="$my_directry/omise_ini.cgi";
	if (! -e $omise_settei_file){
		open(OIB,">$omise_settei_file") || &error("Write Error : $omise_settei_file");
		eval{ flock (OIB, 2); };
		chmod 0666,"$omise_settei_file";
		close(OIB);
	}
	$omise_log_file="$my_directry/omise_log.cgi";
	if (! -e $omise_log_file){
		open(OIL,">$omise_log_file") || &error("Write Error : $omise_log_file");
		eval{ flock (OIL, 2); };
		chmod 0666,"$omise_log_file";
		close(OIL);
	}
		open(OIB,"< $omise_settei_file") || &error("Open Error : $omise_settei_file");
		eval{ flock (OIB, 1); };
			$omise_settei_data = <OIB>;
			($omise_title,$omise_come,$omise_body_style,$omise_syubetu,$omise_table1_style,$omise_table2_style,$omise_koumokumei,$omise_syouhin_table,$omise_title_style,$omise_leed_style,$omise_siasenbako,$omise_yobi5,$omise_yobi6,$omise_yobi7,$omise_yobi8,$omise_yobi9,$omise_yobi10)= split(/<>/,$omise_settei_data);
#omise_yobi5＝基本販売掛け率　omise_yobi6＝商品カテゴリーのスタイル設定　omise_yobi7＝リンクのスタイル
		close(OIB);
		
#スタイルの初期化
	if ($omise_yobi5 eq ""){$omise_yobi5 = "2";}
	if ($omise_body_style eq ""){$omise_body_style = "background-color:#ffcc33;";$syokika =1;} #koko2007/03/21
	if ($omise_title_style eq ""){$omise_title_style = "font-size: 18px; color: #ff6600; line-height:160%;";}
	if ($omise_leed_style eq ""){$omise_leed_style = "font-size: 11px; line-height: 16px; color: #000000";}
	if ($omise_table1_style eq ""){$omise_table1_style = "font-size: 11px; line-height: 18px; color: #666666; background-color:#ffffff; border: #666666; border-style: solid; border-width:1px";}
	if ($omise_table2_style eq ""){$omise_table2_style = "font-size: 10px; color: #336699; background-color:#ffffff; border: #666666; border-style: solid; border-width:1px";}
	if ($omise_syouhin_table eq ""){$omise_syouhin_table = "font-size: 11px; color: #333333; background-color:#ffffaa; ";}
	if ($omise_koumokumei eq ""){$omise_koumokumei = "font-size: 11px; color: #666666; background-color:#ffcc66; ";}
	if ($omise_yobi6 eq ""){$omise_yobi6 = "background-color:#ffff88;";}
	if ($omise_yobi7 eq ""){$omise_yobi7 = "font-size: 11px; color:#333333;text-decoration: none";}
	if ($omise_siasenbako eq ""){$omise_siasenbako = "font-size:11px;color:#000000";}
	print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
	<tr><td>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="omise_settei_do">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<div class=tyuu>■お店の設定</div>
	●お店のタイトル（タグ指定可。絶対URLならばイメージ画像の指定も可）<br>
	<textarea  cols=80 rows=4 name="title" wrap="soft">$omise_title</textarea><br>
	●お店の種類（スーパーは全ての商品を扱うことができますが、仕入れ額が表\示価格の1.5倍になります。また、あとでお店の種類を変えた場合、現在仕入れてある商品は全て無くなりますのでご注意ください。）<br>
	<select name="omise_syubetu">
EOM
	foreach (@global_syouhin_syubetu){
		print "<option value=$_";
		if ($omise_syubetu eq "$_"){print " selected"; $ori_ie_syubetu_0 = $omise_syubetu;} #koko2007/03/17
		print ">$_</option>\n";
	}
	print <<"EOM";
	</select>
	<br>
	●お店のコメント<br>
	<textarea  cols=80 rows=3 name="comento" wrap="soft">$omise_come</textarea><br>
	●基本販売掛け率（デパートでは仕入れ値の３倍の金額で売られています。この価格より高く設定することはできません。商品リストで個別に設定することもできます）<br>
	<input type=text name="omise_yobi5" size=120  value=$omise_yobi5><br>
	●背景のスタイル設定<br>
	<input type=text name="omise_body_style" size=120 value="$omise_body_style"><br>
	●タイトルのスタイル設定<br>
	<input type=text name="omise_title_style" size=120 value="$omise_title_style"><br>
	●コメントのスタイル設定<br>
	<input type=text name="omise_leed_style" size=120 value="$omise_leed_style"><br>
	●タイトル部テーブルのスタイル設定<br>
	<input type=text name="omise_table1_style" size=120 value="$omise_table1_style"><br>
	●商品リストテーブルの枠および凡例のスタイル設定<br>
	<input type=text name="omise_table2_style" size=120 value="$omise_table2_style"><br>
	●商品リストテーブル内スタイル設定<br>
	<input type=text name="omise_syouhin_table" size=120 value="$omise_syouhin_table"><br>
	●商品リストの項目名部分のスタイル設定<br>
	<input type=text name="omise_koumokumei" size=120 value="$omise_koumokumei"><br>
	●商品カテゴリー部分のスタイル設定<br>
	<input type=text name="omise_yobi6" size=120 value="$omise_yobi6"><br>
	●inputとselectのスタイル設定<br>
	<input type=text name="omise_siasenbako" size=120 value="$omise_siasenbako"><br>
	●aタグのスタイル設定<br>
	<input type=text name="omise_yobi7" size=120 value="$omise_yobi7"><br>
	<input type=submit value=設定変更>
	<a href="$this_script?mode=houmon&ori_ie_id=$in{'iesettei_id'}&name=$in{'name'}&pass=$in{'pass'}&con_sele=1" target=_blank>[現在の設定内容の確認]</a><br><br>
	</form>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="my_syouhin">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="仕入れた商品のリスト">
	</form>
	<form method=POST action="$script">
	<input type=hidden name=mode value="orosi">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="仕入れに出かける">（街の卸問屋に行く）</form>
	<!-- koko2007/08/11 -->
	<form method="POST" action="tonyahenpin.cgi">
	<input type=hidden name=mode value="henpin">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="返品を行う"></form>
	</td></tr></table>
EOM
#koko2007/03/21
	if ($syokika){
		$omise_settei_temp = "$omise_title<>$omise_come<>$omise_body_style<>$omise_syubetu<>$omise_table1_style<>$omise_table2_style<>$omise_koumokumei<>$omise_syouhin_table<>$omise_title_style<>$omise_leed_style<>$omise_siasenbako<>$omise_yobi5<>$omise_yobi6<>$omise_yobi7<>$omise_yobi8<>$omise_yobi9<>$omise_yobi10<>\n";
		open(OLOUT,">$omise_settei_file") || &error("$omise_settei_fileに書き込みが出来ません");
		eval{ flock (OLOUT, 2); };
		print OLOUT $omise_settei_temp;
		close(OLOUT);
	}#kokoend2007/03/21
#koko2007/03/17
	open(IN,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
	eval{ flock (IN, 1); };
	@ori_ie_para = <IN>;
	close(IN);
	@new_ori_ie_list3 = (); #koko2007/07/11
	foreach (@ori_ie_para){
		&ori_ie_sprit($_);
		if ($in{'iesettei_id'} eq $ori_k_id){		#ver.1.3
			$ori_ie_syubetu = $ori_ie_syubetu_0;
		}
		&ori_ie_temp;
		push (@new_ori_ie_list3,$ori_ie_temp);#koko2007/03/23
	}
#家リスト更新
#koko2007/09/15
		$i=0;
		$nijyuu = 0;
		foreach (@new_ori_ie_list3){
			if ($_ eq $new_ori_ie_list3[0] && $i){
				$nijyuu = $i;
				&error("二重書き込み o_h 3");
				last;
			}
			$i++;
		}
		if ($nijyuu){
			splice @new_ori_ie_list3,$nijyuu;
		}
#kokoend

	open(OIO,">$ori_ie_list") || &error("$ori_ie_listに書き込めません");
	eval{ flock (OIO, 2); };
	print OIO @new_ori_ie_list3;#koko2007/03/23
	close(OIO);
#kokoend3/17
}

sub omise_settei_do {
	$omise_settei_file="./member/$in{'iesettei_id'}/omise_ini.cgi";
		open(OIB,"< $omise_settei_file") || &error("Open Error : $omise_settei_file");
		eval{ flock (OIB, 1); };
			$omise_settei_data = <OIB>;
			($omise_title,$omise_come,$omise_body_style,$omise_syubetu,$omise_table1_style,$omise_table2_style,$omise_koumokumei,$omise_syouhin_table,$omise_title_style,$omise_leed_style,$omise_siasenbako,$omise_yobi5,$omise_yobi6,$omise_yobi7,$omise_yobi8,$omise_yobi9,$omise_yobi10)= split(/<>/,$omise_settei_data);
		close(OIB);
		
		&lock;
			$change_syubetu_flag = "";
			$omise_title = $in{'title'};
			$omise_come = $in{'comento'};
			if ($omise_syubetu ne $in{'omise_syubetu'}){$change_syubetu_flag = "on";}
			$omise_syubetu = $in{'omise_syubetu'};
			$omise_body_style = $in{'omise_body_style'};
			$omise_table1_style = $in{'omise_table1_style'};
			$omise_table2_style = $in{'omise_table2_style'};
			$omise_koumokumei = $in{'omise_koumokumei'};
			$omise_syouhin_table = $in{'omise_syouhin_table'};
			$omise_title_style = $in{'omise_title_style'};
			$omise_leed_style = $in{'omise_leed_style'};
			$omise_siasenbako = $in{'omise_siasenbako'};
			if ($in{'omise_yobi5'} > 3){&error("販売掛け率は3倍以下にしてください");}
			if ($in{'omise_yobi5'} <= 0){&error("販売掛け率が不適切です。");}			#ver.1.3
			$omise_yobi5 = $in{'omise_yobi5'};
			$omise_yobi6 = $in{'omise_yobi6'};
			$omise_yobi7 = $in{'omise_yobi7'};
			$omise_yobi8 = $in{'omise_yobi8'};
			$omise_yobi9 = $in{'omise_yobi9'};
			$omise_yobi10 = $in{'omise_yobi10'};
		$omise_settei_temp = "$omise_title<>$omise_come<>$omise_body_style<>$omise_syubetu<>$omise_table1_style<>$omise_table2_style<>$omise_koumokumei<>$omise_syouhin_table<>$omise_title_style<>$omise_leed_style<>$omise_siasenbako<>$omise_yobi5<>$omise_yobi6<>$omise_yobi7<>$omise_yobi8<>$omise_yobi9<>$omise_yobi10<>\n";
	open(OLOUT,">$omise_settei_file") || &error("$omise_settei_fileに書き込みが出来ません");
	eval{ flock (OLOUT, 2); };
	print OLOUT $omise_settei_temp;
	close(OLOUT);
#お店の種類変更なら商品リストを初期化
		if ($change_syubetu_flag eq "on"){
			$i = ""; 
			$omise_log_file="./member/$in{'iesettei_id'}/omise_log.cgi";
			open(SP,">$omise_log_file") || &error("Open Error : $omise_log_file");
			eval{ flock (SP, 2); };
			print SP $i;
			close(SP);
		}
		&unlock;
		&my_house_settei;
}


####独自URLの設定
sub dokuzi_settei {
	$my_directry = "./member/$in{'iesettei_id'}";
	$dokuzi_settei_file="$my_directry/dokuzi_ini.cgi";
	if (! -e $dokuzi_settei_file){
		open(OIB,">$dokuzi_settei_file") || &error("Write Error : $dokuzi_settei_file");
		eval{ flock (OIB, 2); };
		chmod 0666,"$dokuzi_settei_file";
		close(OIB);
	}
		open(OIB,"< $dokuzi_settei_file") || &error("Open Error : $dokuzi_settei_file");
		eval{ flock (OIB, 1); };
			$dokuzi_settei_data = <OIB>;
			($dokuzi_url,$dokuzi_width,$dokuzi_height,$dokuzi_haikei_style,$dokuzi_title,$dokuzi_come,$dokuzi_title_style,$dokuzi_leed_style,$dokuzi_siasenbako,$dokuzi_yobi10)= split(/<>/,$dokuzi_settei_data);
		close(OIB);
		
#スタイルの初期化
	if ($dokuzi_haikei_style eq ""){$dokuzi_haikei_style = "background-color:#ffffff;";$syokika =1;} #koko2007/03/21
	if ($dokuzi_title_style eq ""){$dokuzi_title_style = "font-size: 16px; color: #666666;line-height:160%;";}
	if ($dokuzi_leed_style eq ""){$dokuzi_leed_style = "font-size: 11px; line-height: 16px; color: #336699";}
	if ($dokuzi_width eq ""){$dokuzi_width = "800";}
	if ($dokuzi_height eq ""){$dokuzi_height = "400";}
	if ($dokuzi_siasenbako eq ""){$dokuzi_siasenbako = "font-size:11px;color:#000000";}
	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="dokuzi_settei_do">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
	<tr><td>
	<div class=tyuu>■独自URLの設定</div>
	●コーナータイトル（タグ指定可。絶対URLならばイメージ画像の指定も可。また指定しなくてもOKです。）<br>
	<textarea  cols=80 rows=4 name="title" wrap="soft">$dokuzi_title</textarea><br>
	●URL指定<br>
	<input type=text name="dokuzi_url" size=120 value="$dokuzi_url"><br>
	●タイトル下のコメント<br>
	<textarea  cols=80 rows=3 name="comento" wrap="soft">$dokuji_come</textarea><br>
	●背景のスタイル設定<br>
	<input type=text name="dokuzi_haikei_style" size=120 value="$dokuzi_haikei_style"><br>
	●タイトルのスタイル設定<br>
	<input type=text name="dokuzi_title_style" size=120 value="$dokuzi_title_style"><br>
	●タイトル下のコメントのスタイル設定<br>
	<input type=text name="dokuzi_leed_style" size=120 value="$dokuzi_leed_style"><br>
	●IFRAMEの横サイズ<br>
	<input type=text name="dokuzi_width" size=120 value="$dokuzi_width"><br>
	●IFRAMEの縦サイズ<br>
	<input type=text name="dokuzi_height" size=120 value="$dokuzi_height"><br>
	●さい銭箱のスタイル設定<br>
	<input type=text name="dokuzi_siasenbako" size=120 value="$dokuzi_siasenbako"><br>
	
	<input type=submit value=設定変更>
	<a href="$this_script?mode=houmon&ori_ie_id=$in{'iesettei_id'}&name=$in{'name'}&pass=$in{'pass'}&con_sele=2" target=_blank>[現在の設定内容の確認]</a>
	</td></tr></table>
	</form>
EOM
#koko2007/03/21
	if ($syokika){
		$dokuzi_settei_temp = "$dokuzi_url<>$dokuzi_width<>$dokuzi_height<>$dokuzi_haikei_style<>$dokuzi_title<>$dokuzi_come<>$dokuzi_title_style<>$dokuzi_leed_style<>$dokuzi_siasenbako<>$dokuzi_yobi10<>\n";
		open(OLOUT,">$dokuzi_settei_file") || &error("$dokuzi_settei_fileに書き込みが出来ません");
		eval{ flock (OLOUT, 2); };
		print OLOUT $dokuzi_settei_temp;
		close(OLOUT);
	}
#kokoend2007/03/21
}

sub dokuzi_settei_do {
	$dokuzi_settei_file="./member/$in{'iesettei_id'}/dokuzi_ini.cgi";
		open(OIB,"< $dokuzi_settei_file") || &error("Open Error : $dokuzi_settei_file");
		eval{ flock (OIB, 1); };
			$dokuzi_settei_data = <OIB>;
			($dokuzi_url,$dokuzi_width,$dokuzi_height,$dokuzi_haikei_style,$dokuzi_title,$dokuzi_come,$dokuzi_title_style,$dokuzi_leed_style,$dokuzi_siasenbako,$dokuzi_yobi10)= split(/<>/,$dokuzi_settei_data);
		close(OIB);
		
		&lock;
			$dokuzi_title = $in{'title'};
			$dokuzi_come = $in{'comento'};
			$dokuzi_url = $in{'dokuzi_url'};
			$dokuzi_haikei_style = $in{'dokuzi_haikei_style'};
			$dokuzi_title_style = $in{'dokuzi_title_style'};
			$dokuzi_leed_style = $in{'dokuzi_leed_style'};
			$dokuzi_width = $in{'dokuzi_width'};
			$dokuzi_height = $in{'dokuzi_height'};
			$dokuzi_siasenbako = $in{'dokuzi_siasenbako'};
			$dokuzi_yobi10 = $in{'dokuzi_yobi10'};
		$dokuzi_settei_temp = "$dokuzi_url<>$dokuzi_width<>$dokuzi_height<>$dokuzi_haikei_style<>$dokuzi_title<>$dokuzi_come<>$dokuzi_title_style<>$dokuzi_leed_style<>$dokuzi_siasenbako<>$dokuzi_yobi10<>\n";
	open(OLOUT,">$dokuzi_settei_file") || &error("$dokuzi_settei_fileに書き込みが出来ません");
	eval{ flock (OLOUT, 2); };
	print OLOUT $dokuzi_settei_temp;
	close(OLOUT);
		&unlock;
		&my_house_settei;
}

#######家の変更
sub house_change{

if($in{'iesuu'} ne "_0" and $in{'iesuu'} ne "_1" and $in{'iesuu'} ne "_2" and $in{'iesuu'} ne "_3" and $in{'iesuu'} ne ""){error("家の選択が不正ですね。");}

if(!$in{'command'} and $in{'iesuu'}){&house_change2;}

	#売却の場合
	$hausu_disp = 1;
	if ($in{'command'} eq "baikyaku"){
		&lock;
		#家リストへの書き込み
		open(IN,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
		eval{ flock (IN, 1); };
		@ori_ie_para = <IN>;
		close(IN);
        
		@new_ori_ie_list = ();
		foreach (@ori_ie_para){
			&ori_ie_sprit($_);
			if ("${k_id}$in{'iesuu'}" eq $ori_k_id){
				#タウン情報書き換え用に情報を取得
				$my_town_is = $ori_ie_town;
				$my_point_is = $ori_ie_sentaku_point;
				#タウン情報に書き込み
				$write_town_data = "./log_dir/townlog". $my_town_is .".cgi";
				open(TWI,"< $write_town_data") || &error("Open Error : $write_town_data");
				eval{ flock (TWI, 1); };
				$hyouzi_town_hairetu = <TWI>;
				close(TWI);
				
				@town_sprit_matrix =  split(/<>/,$hyouzi_town_hairetu);
				($ori_ie_para_moto,$akichi) = split(/=/, $town_sprit_matrix[$my_point_is]);
				($ori_k_id_in,$syurui,$ori_k_no_in) = split(/_/, $ori_ie_para_moto);
				if (!$akichi){$akichi = "空地";}
				$town_sprit_matrix[$my_point_is] = "$akichi";
                
				$town_temp=join("<>",@town_sprit_matrix);
				#タウン情報更新
				open(TWO,">$write_town_data") || &error("$write_town_dataに書き込めません");
				eval{ flock (TWO, 2); };
				print TWO $town_temp;
				close(TWO);
				
				if ($baikyku_syoumetu eq 'yes'){
					if (-e "./member/$ori_k_id_in/0_log.cgi") {unlink ("./member/$ori_k_id_in/0_log.cgi");}
					if (-e "./member/$ori_k_id_in/1_log.cgi") {unlink ("./member/$ori_k_id_in/1_log.cgi");}
					if (-e "./member/$ori_k_id_in/2_log.cgi") {unlink ("./member/$ori_k_id_in/2_log.cgi");}
					if (-e "./member/$ori_k_id_in/3_log.cgi") {unlink ("./member/$ori_k_id_in/3_log.cgi");}
				}
				
				$ie_atta_flag=1;
				next;
			}
			&ori_ie_temp;
			push (@new_ori_ie_list,$ori_ie_temp);
		}
		if(!$ie_atta_flag){&error("なにかの不具合で家がみつからなかったようです・・・。");}

		#家リスト更新
		$i=0;
		$nijyuu = 0;
		foreach (@new_ori_ie_list){
			if ($_ eq $new_ori_ie_list[0] && $i){
				$nijyuu = $i;
				&error("二重書き込み o_h 4");
				last;
			}
			$i++;
		}
		if ($nijyuu){
			splice @new_ori_ie_list,$nijyuu;
		}
        
		open(OIO,">$ori_ie_list") || &error("$ori_ie_listに書き込めません");
		eval{ flock (OIO, 2); };
		print OIO @new_ori_ie_list;
		close(OIO);
        
		if(!$in{'iesuu'}){
			open(IN,"< ./member/$k_id/oriie_settei.cgi") || &error("Open Error : ./member/$k_id/oriie_settei.cgi");
			eval{ flock (IN, 1); };
			$ie_dat = <IN>;
			close(IN);
			
			(@ie_hairet) = split(/<>/, $ie_dat);
			$ie_hairet[0] = "";
			$ie_hairet[1] = "";
			$ie_hairet[2] = "";
			$ie_hairet[3] = "";
			$ie_dat = join("<>",@ie_hairet);
			
			open(IN,"> ./member/$in{'k_id'}/oriie_settei.cgi") || &error("Open Error : ./member/$in{'k_id'}/oriie_settei.cgi");
			eval{ flock (IN, 2); };
			print IN $ie_dat;
			close(IN);
		}
#kokoend
#ニュース記録
		if($machikakushi eq 'yes'){#koko2007/10/21
			if(!($town_hairetu[$my_town_is] eq $kakushimachi_name && $kakushimachi_name) || !($town_hairetu[$my_town_is] eq $kakushimachi_name1 && $kakushimachi_name1) || !($town_hairetu[$my_town_is] eq $kakushimachi_name2 && $kakushimachi_name2) || !($town_hairetu[$my_town_is] eq $kakushimachi_name3 && $kakushimachi_name3) || !($town_hairetu[$my_town_is] eq $kakushimachi_name4 && $kakushimachi_name4)){
			#	if (!($town_hairetu[$my_town_is] eq $kakushimachi_name)){ #koko2007/06/13
					&news_kiroku("家","$nameさんが「$town_hairetu[$my_town_is]」の家を売却しました。");	#ver.1.3
			#	}
			}
		}else{
			&news_kiroku("家","$nameさんが「$town_hairetu[$my_town_is]」の家を売却しました。");	#ver.1.3
		}
		&unlock;
#ログ更新
		if ($in{'pass'} ne "$admin_pass" || $in{'name'} ne "$admin_name"){
			$money += $town_tika_hairetu[$my_town_is] * 10000;
		}
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);
			
		&header("","sonomati");
		print <<"EOM";
<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
家を売却しました。
</span>
</td></tr></table>
<br>
<form method=POST action="$script">
<input type=hidden name=mode value="login_view">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="戻る">
</form></div>

</body></html>
EOM
		exit;
	}
#変更処理
	if ($in{'command'} eq "do_change"){
		if ($in{'matirank2'} eq ""){&error("家のランクが選択されていません");} #koko2007/08/02
		$kensetu_hiyou = ($ie_hash{$in{'iegazou'}} + $housu_nedan[$in{'matirank2'}])*10000;#koko2007/08/02
		if ($in{'pass'} ne "$admin_pass" || $in{'name'} ne "$admin_name"){
			if ($kensetu_hiyou > $money){&error("お金が足りません。");}
		}
		&lock;
#家リストへの書き込み
		open(IN,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
		eval{ flock (IN, 1); };
		@ori_ie_para = <IN>;
		close(IN);
		@new_ori_ie_list4 = (); #koko2007/07/11
		foreach (@ori_ie_para){
			&ori_ie_sprit($_);
			if ($in{'iesettei_id'} eq $ori_k_id){		#ver.1.3
				if ($in{'iegazou'} ne ""){
					$ori_ie_image = "$img_dir/$in{'iegazou'}";
				}
				if ($in{'matirank2'} ne "99"){#koko2007/08/02
					$ori_ie_rank2 = $in{'matirank2'};#koko2007/08/02
				}
			}
			&ori_ie_temp;
			push (@new_ori_ie_list4,$ori_ie_temp);#koko2007/03/23
		}
#家リスト更新
#koko2007/09/15
		$i=0;
		$nijyuu = 0;
		foreach (@new_ori_ie_list4){
			if ($_ eq $new_ori_ie_list4[0] && $i){
				$nijyuu = $i;
				&error("二重書き込み o_h 5");
				last;
			}
			$i++;
		}
		if ($nijyuu){
			splice @new_ori_ie_list4,$nijyuu;
		}
#kokoend

		open(OIO,">$ori_ie_list") || &error("$ori_ie_listに書き込めません");
		eval{ flock (OIO, 2); };
		print OIO @new_ori_ie_list4;#koko2007/03/23
		close(OIO);

		&unlock;
#ログ更新
		if ($in{'pass'} ne "$admin_pass" || $in{'name'} ne "$admin_name"){
			$money -= $kensetu_hiyou;
		}
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);
			
		&header;
		print <<"EOM";
<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
家の変更をしました。
</span>
</td></tr></table>
<br>
	<form method=POST action="$script">
	<input type=hidden name=mode value="login_view">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="戻る">
	</form></div>

	</body></html>
EOM
		exit;
	}		#変更処理の場合の閉じ
	
#家画像をハッシュから展開
	&header(kentiku_style);
#koko2007/03/30
	@ie_keys = (); #koko2007/07/11
	@ie_values = (); #koko2007/07/11
	if ($in{'town_no'} eq $tokusyu_ie_no && $tokusyu_ie_no ne ''){
		while(($ie_key,$ie_val) = each %ie_hash2){
			push @ie_keys,$ie_key;
			push @ie_values,$ie_val;

		}
	}else{
		while(($ie_key,$ie_val) = each %ie_hash){
			push @ie_keys,$ie_key;
			push @ie_values,$ie_val;
		}
	}
#kokoend
	@ie_rank=@ie_keys[ sort {$ie_values[$a] <=> $ie_values[$b]} 0..$#ie_keys]; #koko2006/03/12

#		sub by_iekey{$ie_values[$a] <=> $ie_values[$b];}
#		@ie_rank=@ie_keys[ sort by_iekey 0..$#ie_keys]; 
	$i=1;
#koko2007/08/14
	if ($in{'town_no'} eq $tokusyu_ie_no && $tokusyu_ie_no ne ''){
		foreach(@ie_rank){
			$iegazou .= "<td align=center><input type=radio name=iegazou value=$_><br><img src=\"$img_dir/$_\" width=32 height=32><br>$ie_hash{$_}万円<br>$name_hash2{$_}\n";
			if ($i % 12 == 0){$iegazou .= "</tr><tr>";}
			$i ++;
		}
	}else{
		foreach(@ie_rank){
			$iegazou .= "<td align=center><input type=radio name=iegazou value=$_><br><img src=\"$img_dir/$_\" width=32 height=32><br>$ie_hash{$_}万円<br>$name_hash{$_}\n";
			if ($i % 12 == 0){$iegazou .= "</tr><tr>";}
			$i ++;
		}
	}
#kokoend
	$iegazou .= "<td align=center><input type=radio name=iegazou value=\"\"><br>現状のまま\n";
	if ($i % 12 == 0){$iegazou .= "</tr><tr>";}
	print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>外観、内装の変更は、建築時と同額の費用がかかります。</td>
	</tr></table><br>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="house_change">
	<input type=hidden name=command value="do_change">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
	<tr><td valign=top>
	<div class=honbun2>●家の選択</div>
	<table boader=0 cellspacing="0" cellpadding="5" width=100%><tr>
	$iegazou
	</tr></table><br>
	
	<table boader=0 cellspacing="0" cellpadding="5" width=100%><tr>
	<td><div class=honbun2>●家のランク（内装費）</div><br>
	<input type=radio name=matirank2 value="0">Ａランク：$housu_nedan[0]万円（４コンテンツ同時表\示が可能\）<br>
	<input type=radio name=matirank2 value="1">Ｂランク：$housu_nedan[1]万円（３コンテンツ同時表\示が可能\）<br>
	<input type=radio name=matirank2 value="2">Ｃランク：$housu_nedan[2]万円（２コンテンツ同時表\示が可能\）<br>
	<input type=radio name=matirank2 value="3">Ｄランク：$housu_nedan[3]万円（１コンテンツ同時表\示が可能\）<br>
	<input type=radio name=matirank2 value="99">現状のまま
	</td></tr></table>
EOM
#上記　name=matirank　→　name=matirank2　に変更　koko2007/08/02
	print <<"EOM";
	<br><br><div align=center><input type=submit value=" OK  "></div>
	</td></tr></table>
	<div align="center"><a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div>
	</body></html>
EOM
	exit;
}

#######家の変更2 Koko2007/08/15
sub house_change2{
#売却の場合
	$hausu_disp = 1;#koko2007/12/14
	if ($in{'iegazou'} eq "baikyaku"){
		&lock;
#家リストへの書き込み
		open(IN,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
		eval{ flock (IN, 1); };
		@ori_ie_para = <IN>;
		close(IN);

		@new_ori_ie_list = ();
		foreach (@ori_ie_para){
			&ori_ie_sprit($_);
			if ($ori_k_id eq "$in{'iesettei_id'}$in{'iesuu'}"){
#タウン情報書き換え用に情報を取得
				$my_town_is = $ori_ie_town;
				$my_point_is = $ori_ie_sentaku_point;
#タウン情報に書き込み
				$write_town_data = "./log_dir/townlog". "$my_town_is" .".cgi"; #koko2007/08/18
				open(TWI,"< $write_town_data") || &error("Open Error : $write_town_data");
				eval{ flock (TWI, 1); };
				$hyouzi_town_hairetu = <TWI>;
				close(TWI);
				@town_sprit_matrix =  split(/<>/,$hyouzi_town_hairetu);
				($ori_ie_para_moto,$akichi) = split(/=/, $town_sprit_matrix[$my_point_is]);
				($ori_k_id_in,$syurui,$ori_k_no_in) = split(/_/, $ori_ie_para_moto);
				if (!$akichi){$akichi = "空地";}
				$town_sprit_matrix[$my_point_is] = "$akichi";#koko2007/05/02
				$town_temp=join("<>",@town_sprit_matrix);
#タウン情報更新
				open(TWO,">$write_town_data") || &error("$write_town_dataに書き込めません");
				eval{ flock (TWO, 2); };
				print TWO $town_temp;
				close(TWO);

				next;
			}
			&ori_ie_temp;
			push (@new_ori_ie_list,$ori_ie_temp);
		}

#家リスト更新
#koko2007/09/15
		$i=0;
		$nijyuu = 0;
		foreach (@new_ori_ie_list){
			if ($_ eq $new_ori_ie_list[0] && $i){
				$nijyuu = $i;
				&error("二重書き込み o_h 6");
				last;
			}
			$i++;
		}
		if ($nijyuu){
			splice @new_ori_ie_list,$nijyuu;
		}
#kokoend


		open(OIO,">$ori_ie_list") || &error("$ori_ie_listに書き込めません");
		eval{ flock (OIO, 2); };
		print OIO @new_ori_ie_list;
		close(OIO);
#ニュース記録
		if($machikakushi eq 'yes'){ #koko2007/10/21
			if(!($town_hairetu[$my_town_is] eq $kakushimachi_name && $kakushimachi_name) || !($town_hairetu[$my_town_is] eq $kakushimachi_name1 && $kakushimachi_name1) || !($town_hairetu[$my_town_is] eq $kakushimachi_name2 && $kakushimachi_name2) || !($town_hairetu[$my_town_is] eq $kakushimachi_name3 && $kakushimachi_name3) || !($town_hairetu[$my_town_is] eq $kakushimachi_name4 && $kakushimachi_name4)){

		#	if (!($town_hairetu[$my_town_is] eq $kakushimachi_name && $machikakushi eq 'yes')){ #koko2007/06/13
				&news_kiroku("家","$nameさんが「$town_hairetu[$my_town_is]」の家を売却しました。");		#ver.1.3
			}
#koko2007/10/29
		}else{ #koko2007/10/30
			&news_kiroku("家","$nameさんが「$town_hairetu[$my_town_is]」の家を売却しました。");		#ver.1.3
		}
		&unlock;
#ログ更新
		if ($in{'pass'} ne "$admin_pass" || $in{'name'} ne "$admin_name"){
			$money += $town_tika_hairetu[$my_town_is] * 10000;
		}
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);
			
		&header("","sonomati");
		print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
家を売却しました。
</span>
</td></tr></table>
<br>
	<form method=POST action="$script">
	<input type=hidden name=mode value="login_view">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="戻る">
	</form></div>

	</body></html>
EOM
		exit;
	}

#変更処理
	if ($in{'command'} eq "do_change2"){
		$kensetu_hiyou = $ie_hash{$in{'iegazou'}};
		if ($in{'pass'} ne "$admin_pass" || $in{'name'} ne "$admin_name"){
			if ($kensetu_hiyou > $money){&error("お金が足りません。");}
		}
		&lock;
#家リストへの書き込み
		$ori_ie_fail = "./log_dir/ori_ie_log.cgi"; #koko2007/08/15
		open(IN,"< $ori_ie_fail") || &error("Open Error : $ori_ie_list"); #koko2007/08/15
		eval{ flock (IN, 1); };
		@ori_ie_para = <IN>;
		close(IN);
		@new_ori_ie_list5 = ();


		foreach (@ori_ie_para){
			&ori_ie_sprit($_);
			if ($ori_k_id eq "$in{'iesettei_id'}$in{'iesuu'}"){
				if ($in{'iegazou'} ne ""){
					$ori_ie_image = "$img_dir/$in{'iegazou'}";
				}
			}
			&ori_ie_temp;
			push (@new_ori_ie_list5,$ori_ie_temp);
		}
#家リスト更新
		open(OIO,">$ori_ie_fail") || &error("$ori_ie_failに書き込めません"); #koko2007/08/15
		eval{ flock (OIO, 2); };
		print OIO @new_ori_ie_list5;
		close(OIO);

		&unlock;
#ログ更新
		if ($in{'pass'} ne "$admin_pass" || $in{'name'} ne "$admin_name"){
			$money -= $kensetu_hiyou;
		}
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);
			
		&header;
		print <<"EOM";
<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
家の変更をしました。
</span>
</td></tr></table>
<br>
	<form method=POST action="$script">
	<input type=hidden name=mode value="login_view">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="戻る">
	</form></div>

	</body></html>
EOM
		exit;
	}		#変更処理の場合の閉じ
#家画像をハッシュから展開
	&header(kentiku_style);
	@ie_keys = ();
	@ie_values = ();
	if ($in{'town_no'} eq $tokusyu_ie_no && $tokusyu_ie_no ne ''){
		while(($ie_key,$ie_val) = each %ie_hash2){
			push @ie_keys,$ie_key;
			push @ie_values,$ie_val;

		}
	}else{
		while(($ie_key,$ie_val) = each %ie_hash){
			push @ie_keys,$ie_key;
			push @ie_values,$ie_val;
		}
	}
	@ie_rank=@ie_keys[ sort {$ie_values[$a] <=> $ie_values[$b]} 0..$#ie_keys]; #koko2006/03/12

	$i=1;
	if ($in{'town_no'} eq $tokusyu_ie_no && $tokusyu_ie_no ne ''){
		foreach(@ie_rank){
			$ie_hash{$_} =int($ie_hash{$_} * $ie_bairitu);
			$iegazou .= "<td align=center><input type=radio name=iegazou value=$_><br><img src=\"$img_dir/$_\" width=32 height=32><br>$ie_hash{$_}万円<br>$name_hash2{$_}\n";
			if ($i % 12 == 0){$iegazou .= "</tr><tr>";}
			$i ++;
		}
	}else{
		foreach(@ie_rank){
			$ie_hash{$_} =int($ie_hash{$_} * $ie_bairitu);
			$iegazou .= "<td align=center><input type=radio name=iegazou value=$_><br><img src=\"$img_dir/$_\" width=32 height=32><br>$ie_hash{$_}万円<br>$name_hash{$_}\n";
			if ($i % 12 == 0){$iegazou .= "</tr><tr>";}
			$i ++;
		}
	}
	$disp_sentaku = $in{'iesuu'} +1;
	$iegazou .= "<td align=center><input type=radio name=iegazou value=\"\"><br>現状のまま\n";
	if ($i % 12 == 0){$iegazou .= "</tr><tr>";}
	print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>外観、内装の変更は、建築時と同額の費用がかかります。</td>
	</tr></table><br>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="house_change2">
	<input type=hidden name=command value="do_change2">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">	
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=iesuu value="$in{'iesuu'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
	<tr><td valign=top>
	<div class=honbun2>●家の選択 $disp_sentaku</div>
	<table boader=0 cellspacing="0" cellpadding="5" width=100%><tr>
	$iegazou
	<td align=center><input type=radio name=iegazou value="baikyaku"><br>売却
	</tr></table><br>
	
	<br><br><div align=center><input type=submit value=" OK  "></div>
	</td></tr></table>
	<div align="center"><a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div>
	</body></html>
EOM
	exit;
}

#####訪問処理
sub houmon {
#koko2007/04/20
	if ($in{'ori_ie_id'} eq "admin"){&normal_bbs;}#koko2007/12/14
	($in{'ori_ie_id'},$bangou) = split(/_/, $in{'ori_ie_id'});
	if ($bangou == 1){&unei_2;} #koko2007/04/21 koko2007/04/30 koko2007/09/08
#kokoend
	if ($bangou == 2){&kaishiya;} #koko2007/05/05
	if ($bangou == 3){&motimono_hanbai;} #koko2007/09/08

	$houmonsaki_settei_file = "./member/$in{'ori_ie_id'}/oriie_settei.cgi";
	open(HS,"< $houmonsaki_settei_file") || &error("まだ工事中です");
	eval{ flock (HS, 1); };
	$kihon_oriie_settei = <HS>;
	&oriie_settei_sprit ($kihon_oriie_settei);
	close(HS);
	if ($my_con1 eq ""){&error("まだ人に見せられる家では無いようです。");}		#ver.1.30
	
#さい銭箱を変数に入れる
$saisenbako_data =<<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="saisensuru">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<select name=saisengaku>
	<option value=100>100円</option>
	<option value=500>500円</option>
	<option value=1000>1000円</option>
	<option value=2000>2000円</option>
	<option value=5000>5000円</option>
	<option value=10000>10000円</option>
	</select>
	<input type=submit value="さい銭する">
	</form>
EOM

	if ($my_con1_title){
		$centents_botan .="<td><form method=POST action=\"$this_script\"><input type=hidden name=mode value=\"houmon\"><input type=hidden name=ori_ie_id value=\"$in{'ori_ie_id'}\"><input type=hidden name=name value=$in{'name'}><input type=hidden name=pass value=\"$in{'pass'}\"><input type=hidden name=k_id value=\"$in{'k_id'}\"><input type=hidden name=con_sele value=\"$my_con1\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><input type=submit value=\"$my_con1_title\"></form></td>\n";
	}
	
	if ($my_con2_title){
		$centents_botan .="<td><form method=POST action=\"$this_script\"><input type=hidden name=mode value=\"houmon\"><input type=hidden name=ori_ie_id value=\"$in{'ori_ie_id'}\"><input type=hidden name=name value=\"$in{'name'}\"><input type=hidden name=pass value=\"$in{'pass'}\"><input type=hidden name=k_id value=\"$in{'k_id'}\"><input type=hidden name=con_sele value=\"$my_con2\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><input type=submit value=\"$my_con2_title\"></form></td>\n";
	}
	
	if ($my_con3_title){
		$centents_botan .="<td><form method=POST action=\"$this_script\"><input type=hidden name=mode value=\"houmon\"><input type=hidden name=ori_ie_id value=\"$in{'ori_ie_id'}\"><input type=hidden name=name value=\"$in{'name'}\"><input type=hidden name=pass value=\"$in{'pass'}\"><input type=hidden name=k_id value=\"$in{'k_id'}\"><input type=hidden name=con_sele value=\"$my_con3\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><input type=submit value=\"$my_con3_title\"></form></td>\n";
	}
	
	if ($my_con4_title){
		$centents_botan .="<td><form method=POST action=\"$this_script\"><input type=hidden name=mode value=\"houmon\"><input type=hidden name=ori_ie_id value=\"$in{'ori_ie_id'}\"><input type=hidden name=name value=\"$in{'name'}\"><input type=hidden name=pass value=\"$in{'pass'}\"><input type=hidden name=con_sele value=\"$my_con4\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><input type=submit value=\"$my_con4_title\"></form></td>\n";
	}
	
	if ($in{'con_sele'} eq ""){
		if ($my_con1 eq "0"){&normal_bbs;}
		elsif  ($my_con1 eq "1"){&omise;}
		elsif  ($my_con1 eq "2"){&dokuzi_url;}
		elsif  ($my_con1 eq "3"){&gentei;}
	}elsif  ($in{'con_sele'} eq "0"){&normal_bbs;}
	elsif  ($in{'con_sele'} eq "1"){&omise;}
	elsif  ($in{'con_sele'} eq "2"){&dokuzi_url;}
	elsif  ($in{'con_sele'} eq "3"){&gentei;}
}

#####通常のBBS
sub normal_bbs {
	if ($tajuukinsi_flag==1){
		if($k_yobi3 ne ""){
			&error("多重登録は禁止されています。<br>$k_yobi3");
		}
	}
	if ($tajuukinsi_flag==1){&tajuucheck;}
#ver.1.30ここから
	$genzai_zikoku = time;
	open(GUEST,"< $guestfile");
	eval{ flock (GUEST, 1); };
	@all_guest=<GUEST>;
	close(GUEST);
	@new_all_guest = ();
	foreach (@all_guest) {
		($sanka_timer,$sanka_name,$hyouzi_check,$mati_name) = split(/<>/);
		if ($name eq "$sanka_name"){
			$sanka_timer = $genzai_zikoku;
		}
		$sanka_tmp = "$sanka_timer<>$sanka_name<>$hyouzi_check<>$mati_name<>\n";
		push (@new_all_guest,$sanka_tmp);
	}
#ver.1.40ここから
	if ($mem_lock_num == 0){
		$err = &data_save($guestfile, @new_all_guest);
		if ($err) {&error("$err");}
	}else{
		&lock;	
		open(GUEST,">$guestfile");
		eval{ flock (GUEST, 2); };
		print GUEST @new_all_guest;
		close(GUEST);
		&unlock;
	}
#ver.1.40ここまで
#ver.1.30ここまで
	if ($in{'ori_ie_id'} eq "admin"){
		$bbs1_settei_file = "./member/admin/bbs".$in{'bbs_num'}."_ini.cgi";
	}else{
		$bbs1_settei_file = "./member/$in{'ori_ie_id'}/bbs1_ini.cgi";
	}
		open(OIB,"< $bbs1_settei_file") || &error("Open Error : $bbs1_settei_file");
		eval{ flock (OIB, 1); };
			$bbs1_settei_data = <OIB>;
			($bbs1_title,$bbs1_come,$bbs1_body_style,$bbs1_toukousya_style,$bbs1_table2_style,$bbs1_toukouwidth,$bbs1_a_hover_style,$bbs1_tablewidth,$bbs1_title_style,$bbs1_leed_style,$bbs1_siasenbako,$bbs1_yobi5,$bbs1_yobi6,$bbs1_yobi7,$bbs1_yobi8,$bbs1_yobi9,$bbs1_yobi10,$bbs_link)= split(/<>/,$bbs1_settei_data);
		close(OIB);
		chomp $bbs_link; #koko2007/06/26
#住民専用掲示板の場合チェック
	if ($bbs1_yobi6 eq "on"){
		if ($in{'admin_pass'} ne $admin_pass){
			&my_town_check($name);
			if ($return_my_town eq "no_town"){&error("この街に住んでいる人以外は見ることができません");}
			if ($return_my_town ne "$in{'town_no'}"){&error("この街に住んでいる人以外は見ることができません");}
		}
	}
	&ori_header("$bbs1_body_style","$bbs1_siasenbako","$bbs1_a_hover_style");

	print <<"EOM";

	<table  border="0" cellspacing="0" cellpadding="5" align=center >
	<tr>$centents_botan<td align=right>$saisenbako_data</td></tr>
	</table>
EOM
	
	print <<"EOM";

	<br><table width="$bbs1_tablewidth" border="0" cellspacing="0" cellpadding="14" align=center style="$bbs1_table2_style">
	<tr><td>
	<div style = "$bbs1_title_style">$bbs1_title</div>
	<div style = "$bbs1_leed_style">$bbs1_come</div>
	</td></tr>
	</table>
<br>
	<table width="$bbs1_tablewidth" border="0" cellspacing="0" cellpadding="14" align=center style="$bbs1_table2_style">
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="bbs_regist">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
	<input type=hidden name=bbs_num value="$in{'bbs_num'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<tr><td>
	<textarea cols="$bbs1_toukouwidth" rows="4" name="b_com" wrap="soft">$in{'b_com'}</textarea>
	<input type=submit value="新規投稿" name="toukou"><br>
	<input type="checkbox" name="mini_icon" value='checked' $in{'mini_icon'}>ミニコン表\示
	<input type=submit value="ミニコン" name="minicon">
EOM
	if($in{'mini_icon'} || $in{'minicon'}){
		print <<"EOM";
	<table>
	<tr>
<td><input type="radio" name=kyara value="[sun]"><img src='img/mini/ic_sun.gif'></td>
<td><input type="radio" name=kyara value="[cloudy]"><img src='img/mini/ic_cloudy.gif'></td>
<td><input type="radio" name=kyara value="[typhoon]"><img src='img/mini/ic_typhoon.gif'></td>
<td><input type="radio" name=kyara value="[rain]"><img src='img/mini/ic_rain.gif'></td>
<td><input type="radio" name=kyara value="[thunder]"><img src='img/mini/ic_thunder.gif'></td>
<td><input type="radio" name=kyara value="[snow]"><img src='img/mini/ic_snow.gif'></td>
<td><input type="radio" name=kyara value="[smoking]"><img src='img/mini/ic_smoking.gif'></td>
<td><input type="radio" name=kyara value="[ribbon]"><img src='img/mini/ic_ribbon.gif'></td>
</tr><tr>
<td><input type="radio" name=kyara value="[fog]"><img src='img/mini/ic_fog.gif'></td>
<td><input type="radio" name=kyara value="[gemini]"><img src='img/mini/ic_gemini.gif'></td>
<td><input type="radio" name=kyara value="[spit]"><img src='img/mini/ic_spit.gif'></td>
<td><input type="radio" name=kyara value="[taurus]"><img src='img/mini/ic_taurus.gif'></td>
<td><input type="radio" name=kyara value="[aries]"><img src='img/mini/ic_aries.gif'></td>
	</tr>
	</table>
EOM
	}
	print <<"EOM";
	</form>
EOM
	$page=$in{'page'};	
	if ($page eq "") { $page = 0; }
	$i=0;
	if ($in{'ori_ie_id'} eq "admin"){
		$bbs1_log_file = "./member/admin/bbs".$in{'bbs_num'}."_log.cgi";
	}else{
		$bbs1_log_file = "./member/$in{'ori_ie_id'}/bbs1_log.cgi";
	}
	open(IN,"< $bbs1_log_file") || &error("Open Error : $bbs1_log_file");
	eval{ flock (IN, 1); };
	@bbs_alldata=<IN>;
	close(IN);
	
	if ($in{'ori_ie_id'} eq $k_id){
		($total_counter,$all_total_counter,$kakikomijikan,$yomidashijikan,$bbs_id)= split(/<>/, $bbs_alldata[0]);
		chomp $bbs_id;
		if ($kakikomijikan > $yomidashijikan){
			$ima_time = time;
			$bbs_alldata[0] = "$total_counter<>$all_total_counter<>$kakikomijikan<>$ima_time<>$bbs_id<>\n";
			open(IN,"> $bbs1_log_file") || &error("Open Error : $bbs1_log_file");
			eval{ flock (IN, 2); };
			print IN @bbs_alldata;
			close(IN);
		}
	}
    
	foreach (@bbs_alldata){
		($b_num,$b_name,$b_date,$b_res,$b_mail,$b_com,$b_id)= split(/<>/);
		($b_name,$iranai) = split(/<span/,$b_name);#古い記事用に分割
		if ($b_num){$i++;}
		if ($i == 1){next;}
		if ($i < $page + 1) { next; }
		if ($i > $page + 10) { last; }
        
		$b_id =~ s/[^0-9]//g;
		if ($b_id ne ""){
			if (not(-e "./member/$b_id/oriie_settei.cgi")){$b_id = "";}
			if ($b_id ne ""){
				open(IN,"< ./member/$b_id/oriie_settei.cgi") || &error("Open Error : ./member/$b_id/oriie_settei.cgi");
				eval{ flock (IN, 1); };
				$ie_dat = <IN>;
				close(IN);
				(@ie_hairet) = split(/<>/, $ie_dat);
				if (!($ie_hairet[0] eq "0" || $ie_hairet[1] eq "0" || $ie_hairet[2] eq "0" || $ie_hairet[3] eq "0")){ $b_id = "";}
			}
		}
        
		if ($b_res){
			if ($b_id ne "" && ($linkbotan eq 'yes' || $bbs_link)){
				print <<"EOM";
<table width="100%" cellpadding="5" cellspacing="0" style="font-size:12px;border: solid 3px #DCDCED;">
<tr bgcolor="#DCDCED">
<td align="left">
	<dt>
		<a name="$b_mail"><span style="$bbs1_toukousya_style"><b>No.$b_mail&nbsp;&nbsp;$b_name</b></span></a>
		<font color="#666666" size="1">（$b_date）</font>
	</dt>
</td></tr>
<tr bgcolor="#ffffff"><td colspan="2">
	<dd>
		$b_com
        <div align="right">
			<table><tr>		
			<form method=POST action="original_house.cgi" style="margin-top:0; margin-bottom:0;">
			<input type="hidden" name="my_data" value="$name<>$pass<>$in{'k_id'}<>$in{'town_no'}<>houmon<>">
			<input type=hidden name=ori_ie_id value="$b_id">
			<input type=hidden name=con_sele value="0">
			<td>
				<input type=image src="./img/house_mini.gif" alt="掲示板に飛びます。">
			</td>
			</form>
			<form method=POST action="./town_maker.cgi" style="margin-top:0; margin-bottom:0;">
			<input type="hidden" name="my_data" value="$name<>$pass<>$in{'k_id'}<>$in{'town_no'}<>mail_sousin<>">
			<input type=hidden name=sousinsaki_name value=$b_name>
			<td>
		    	<input type=image src="./img/mail_mini.gif" alt="メールを送信します。">
			</td>
			</form>
			</tr>
			</table>
		</div>
	</dd>
</td></tr></table>
<br>
EOM
			}else{
				print <<"EOM";
<table width="100%" cellpadding="5" cellspacing="0" style="font-size:12px;border: solid 3px #DCDCED;">
<tr bgcolor="#DCDCED"><td align="left">
	<dt>
		<a name="$b_mail"><span style="$bbs1_toukousya_style"><b>No.$b_mail&nbsp;&nbsp;$b_name</b></span></a>
		<font color="#666666" size="1">（$b_date）</font>
	</dt>
</td></tr>
<tr bgcolor="#ffffff"><td colspan="2">
	<dd>
		$b_com
        <div align="right">
			<table><tr>
		    <form method=POST action="./town_maker.cgi" style="margin-top:0; margin-bottom:0;">
			<input type="hidden" name="my_data" value="$name<>$pass<>$in{'k_id'}<>$in{'town_no'}<>mail_sousin<>">
			<input type=hidden name=sousinsaki_name value=$b_name>
			<td>
				<input type=image src="./img/mail_mini.gif" alt="メールを送信します。">
			</td>
			</form>
			</tr></table>
		</div>
	</dd>
</td></tr></table>
<br>
EOM
			}
		}else{
			print <<"EOM";
	</dl><dl>
</td></tr></table>
<br>
<table width="$bbs1_tablewidth" border="0" cellspacing="0" cellpadding="14" align=center style="$bbs1_table2_style">
<tr><td>
    <span style="$bbs1_yobi5">NO.$b_num</span><br>
EOM
			if ($b_id ne "" && ($linkbotan eq 'yes' || $bbs_link)){
				print <<"EOM";
<table width="100%" cellpadding="5" cellspacing="0" style="font-size:12px;border: solid 3px #8080C0;">
<tr bgcolor="#8080C0"><td align="left">
	<dt>	
		<a name="$b_mail"><span style="$bbs1_toukousya_style"><b><font color="#ffffff">No.$b_mail&nbsp;&nbsp;$b_name</font></b></span></a>
		<font color="#ffffff" size="1">（$b_date）</font>
	</dt>
</td></tr>
<tr bgcolor="#ffffff"><td colspan="2">
	<dd>
		$b_com
        <div align="right">		
			<table><tr>
			<form method=POST action="original_house.cgi" style="margin-top:0; margin-bottom:0;">
			<input type="hidden" name="my_data" value="$name<>$pass<>$in{'k_id'}<>$in{'town_no'}<>houmon<>">
			<input type=hidden name=ori_ie_id value="$b_id">
			<input type=hidden name=con_sele value="0">
			<td>
				<input type=image src="./img/house_mini.gif" alt="掲示板に飛びます。">
			</td>
			</form>
			<form method=POST action="./town_maker.cgi" style="margin-top:0; margin-bottom:0;">
			<input type="hidden" name="my_data" value="$name<>$pass<>$in{'k_id'}<>$in{'town_no'}<>mail_sousin<>">
			<input type=hidden name=sousinsaki_name value=$b_name>
			<td>
				<input type=image src="./img/mail_mini.gif" alt="メールを送信します。">
			</td>
			</form>
			</tr></table>
		</div>
	</dd>
</td></tr></table>
<br>
EOM
			}else{
				print <<"EOM";
<table width="100%" cellpadding="5" cellspacing="0" style="font-size:12px;border: solid 3px #8080C0;">
<tr bgcolor="#8080C0"><td align="left">
	<dt>	
		<a name="$b_mail"><span style="$bbs1_toukousya_style"><b><font color="#ffffff">No.$b_mail&nbsp;&nbsp;$b_name</font></b></span></a>
		<font color="#ffffff" size="1">（$b_date）</font>
	</dt>
</td></tr>
<tr bgcolor="#ffffff"><td colspan="2">
	<dd>
		$b_com
        <div align="right">		
			<table><tr>
			<form method=POST action="./town_maker.cgi" style="margin-top:0; margin-bottom:0;">
			<input type="hidden" name="my_data" value="$name<>$pass<>$in{'k_id'}<>$in{'town_no'}<>mail_sousin<>">
			<input type=hidden name=sousinsaki_name value=$b_name>
			<td>
				<input type=image src="./img/mail_mini.gif" alt="メールを送信します。">
			</td>
			</form>
			</tr></table>
		</div>
	</dd>
</td></tr></table>
<br>
EOM
			}
			print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="bbs_regist">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
	<input type=hidden name=bbs_num value="$in{'bbs_num'}">
	<input type=hidden name=b_res value="$b_num">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<textarea rows=2 name=b_com cols=50 ></textarea> <input type=submit value="レス">
	</form>
EOM
		}
	}		#foreach閉じ
	
		$next = $page + 10;
		$back = $page - 10;
		print "<div align=center><table border=0><tr>";
		if ($back >= 0) {
#管理者BBSの場合
				if($in{'ori_ie_id'} eq "admin"){
					print <<"EOM";
			<form method=POST action="$this_script">
			<input type=hidden name=mode value="normal_bbs">
			<input type=hidden name=ori_ie_id value="admin">
			<input type=hidden name=bbs_num value="$in{'bbs_num'}">
<input type=hidden name=k_id value="$in{'k_id'}">
			<input type=hidden name=name value="$in{'name'}">
			<input type=hidden name=pass value="$in{'pass'}">
			<input type=hidden name=town_no value="$in{'town_no'}">
			<input type=hidden name=page value="$back">
			<input type=submit value="BACK">
			</form>
EOM
				}else{
#個人の家のBBSの場合
					print <<"EOM";
			<td><form method="POST" action="$this_script">
			<input type=hidden name=mode value="houmon">
			<input type=hidden name=con_sele value="0">
			<input type=hidden name=name value="$in{'name'}">
			<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
			<input type=hidden name=town_no value="$in{'town_no'}">
			<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
			<input type=hidden name=page value="$back">
			<input type=submit value="BACK"></form></td>
EOM
				}
		}
		if ($next < $i) {
				if($in{'ori_ie_id'} eq "admin"){
					print <<"EOM";
			<form method=POST action="$this_script">
			<input type=hidden name=mode value="normal_bbs">
			<input type=hidden name=ori_ie_id value="admin">
			<input type=hidden name=bbs_num value="$in{'bbs_num'}">
			<input type=hidden name=name value="$in{'name'}">
			<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
			<input type=hidden name=town_no value="$in{'town_no'}">
			<input type=hidden name=page value="$next">
			<input type=submit value="NEXT">
</form>
EOM
				}else{
					print <<"EOM";
			<td><form method="POST" action="$this_script">
			<input type=hidden name=mode value="houmon">
			<input type=hidden name=con_sele value="0">
			<input type=hidden name=name value="$in{'name'}">
			<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
			<input type=hidden name=town_no value="$in{'town_no'}">
			<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
			<input type=hidden name=page value="$next">
			<input type=submit value="NEXT"></form></td>
EOM
				}
		}
		print "</tr></table></div>";
	print <<"EOM";
	</td></tr></table>
	<table width="$bbs1_tablewidth" border="0" cellspacing="0" cellpadding="0" align=center>
	<tr><td>
	<form method="POST" action="$this_script">
	<div style=" font-size: 10px; color: #444444"><br>
	<center>
	<input type=hidden name=mode value="bbs_delete">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
	<input type=hidden name=bbs_num value="$in{'bbs_num'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	記事no. <input type=text name=b_count size=8>
	<input type=submit value="削除">

	親記事no. <input type=text name=oya_count size=8>
	<input type=submit value="削除">
	<input type=submit name= all_del value=" 全記事削除" >

	</center>
	<br>※ゲーム管理者のみ「記事no.」を指定して記事を削除することができます。<br>
	※投稿することでお金を得ることができますが、無意味な発言、荒らし行為など不適切な投稿があった場合、減金、ホストの公開、アクセス拒否などのペナルティがありますのでご注意ください。</div>
	</form></td></tr><tr><td>
	<br><div style=" font-size: 11px;" align="center"><a href="javascript:history.back()"> [前の画面に戻る] </a></div>
	</td></tr>
	</table>
EOM
	if ($in{'ori_ie_id'} eq "admin"){
		&hooter("login_view","戻る");
	}else{
		&hooter("login_view","家を出る");
	}
exit;
}


#BBS投稿処理
sub bbs_regist {
	if(!$in{'toukou'} && ($in{'kyara'} || $in{'mini_icon'} || $in{'minicon'})){$in{'b_com'} = "$in{'b_com'}$in{'kyara'}";$in{'mode'}='normal_bbs';$in{'con_sele'}=0;&houmon;exit;}#koko2007/12/14

	&lock;
#ログファイル更新
	# ログを読み込み
	if ($in{'ori_ie_id'} eq "admin"){
		$bbs1_log_file = "./member/admin/bbs".$in{'bbs_num'}."_log.cgi";
	}else{
		$bbs1_log_file = "./member/$in{'ori_ie_id'}/bbs1_log.cgi";
	}
	open(IN,"< $bbs1_log_file") || &error("Open Error : $bbs1_log_file");
	eval{ flock (IN, 1); };
	# 先頭行を取得
	$total_counter = <IN>;
	($total_counter,$all_total_counter,$kakikomijikan,$yomidashijikan,$bbs_id) = split(/<>/, $total_counter);		#ver.1.40
	chomp $bbs_id;
	$top = <IN>;
	local($b_num,$b_name,$b_date,$b_res,$b_count,$b_com,$b_id)= split(/<>/, $top);#koko2006/12/11		#ver.1.40
	close(IN);

	if (length($in{'b_com'}) > 500) {&error("挨拶は全角250字半角500字以内です");} #koko2006/12/12

	
	$in{'b_com'} =~ s/<>/&lt;&gt;/g;

#タグ禁止処理
#		$in{'b_com'} =~ s/</&lt;/g;
#		$in{'b_com'} =~ s/>/&gt;/g;
# コメントの改行処理
	$in{'b_com'} =~ s/\r\n/<br>/g;
	$in{'b_com'} =~ s/\r/<br>/g;
	$in{'b_com'} =~ s/\n/<br>/g;
	$in{'b_com'} =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<a href=\"$2\" target=\"_blank\">$2<\/a>/g;
		
	if ($in{'name'} eq "$b_name" && $in{'b_com'} eq "$b_com") {
		&error("二重投稿です");
	}
	if ($in{'b_com'} eq "") {
		&error("コメントが入力されていません");
	}

	open(IN,"< $bbs1_log_file") || &error("Open Error : $bbs1_log_file");
	eval{ flock (IN, 1); };
	@all_data = <IN>;
	shift @all_data;
	$total_kizisuu = @all_data;
	close(IN);

	&time_get;
	$all_total_counter ++;
#新規投稿なら新記事Noを取得
	if ($in{'b_res'} eq ""){
		$total_counter++;
		$new_toukou = "$total_counter<>$in{'name'}<>$date2<>$in{'b_res'}<>$all_total_counter<>$in{'b_com'}<>$in{'k_id'}<>\n";
		unshift (@all_data,$new_toukou);
		
		$ima_time = time;
		$total_counter = "$total_counter<>$all_total_counter<>$ima_time<>$yomidashijikan<>$in{'k_id'}<>\n";
		unshift (@all_data,$total_counter);
#レスの場合
	}else{
			$new_toukou = "<>$in{'name'}<>$date2<>$in{'b_res'}<>$all_total_counter<>$in{'b_com'}<>$in{'k_id'}<>\n";
		foreach (@all_data){
			($b_num,$b_name,$b_date,$b_res,$b_mail,$b_com,$b_id)= split(/<>/, $_);
			if ($b_num eq "$in{'b_res'}" || $b_res eq "$in{'b_res'}"){
			       push (@top_idou ,$_);
			       $mail_count++;
			       next;
			       }
			push (@new_all_data,$_);
		}
			($mae_num,$mae_name,$mae_date,$mae_res,$mae_mail,$mae_com,$mae_id)= split(/<>/, $top_idou[$mail_count-1]);
			if($name eq $mae_name){
				if($in{'b_com'} eq $mae_com){
					&error("二重投稿です");
				}
				$renzoku = "yes";
		    }

		push (@top_idou ,$new_toukou);	
        
		$ima_time = time;
		unshift (@new_all_data,@top_idou);
		$total_counter = "$total_counter<>$all_total_counter<>$ima_time<>$yomidashijikan<>$in{'k_id'}<>\n";
        
		unshift (@new_all_data,$total_counter);
		@all_data = ();
		@all_data = @new_all_data;
	}
	
	if ($total_kizisuu >= $bbs_kizi_max){pop @all_data;}
	
	open(OUT,">$bbs1_log_file") || &error("Write Error : $bbs1_log_file");
	eval{ flock (OUT, 2); };
	print OUT @all_data;
	close(OUT);
	
#街の繁栄度アップ
	&town_haneiup($in{'town_no'});

# ロック解除
	&unlock;
	
#お金をゲット
	$randed += int(rand(10))+1;
	if($renzoku eq "yes"){
			$message_in = "●連続投稿なのでお金もらえまへんでした。";
	}else{
		if ($randed == 7){
				$coupon_rand2 = int(rand(5))+1;
			&coupon_get($coupon_rand2);
			$randed += int(rand(10000))+5000;
			$money += $randed;
			$kpoint+=3;
			$message_in = "●ボーナスです！$randed円のお金をゲットしました。<br>★クーポン券を$coupon_rand2枚もらいました！<br>★評価ポイントを３ＰＧＥＴしました！";
		}else{
			$randed += int(rand(2000))+1000;
			$money += $randed;
			$message_in = "●$randed円のお金を得ました。";
		}
	}
	
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
	&header("","sonomati");
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
投稿しました。<br>
$message_in
</span>
</td></tr></table>
<br>
	<form method=POST action="$this_script">
EOM
	if ($in{'ori_ie_id'} eq "admin"){
		print "<input type=hidden name=mode value=\"normal_bbs\">";
	}else{
		print "<input type=hidden name=mode value=\"houmon\">";
	}

	print <<"EOM";
	<input type=hidden name=con_sele value="0">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
	<input type=hidden name=bbs_num value="$in{'bbs_num'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="戻る">
	</form></div>
EOM
	exit;
}

#####家主掲示板
sub gentei {
	$gentei_settei_file = "./member/$in{'ori_ie_id'}/gentei_ini.cgi";
		open(OIB,"< $gentei_settei_file") || &error("Open Error : $gentei_settei_file");
		eval{ flock (OIB, 1); };
			$gentei_settei_data = <OIB>;
			($gentei_title,$gentei_come,$gentei_body_style,$gentei_daimei_style,$gentei_table2_style,$gentei_kensuu,$gentei_tablewidth,$gentei_title_style,$gentei_leed_style,$gentei_siasenbako,$gentei_yobi5,$gentei_yobi6,$gentei_yobi7,$gentei_yobi8,$gentei_yobi9,$gentei_yobi10)= split(/<>/,$gentei_settei_data);
		close(OIB);
	&ori_header("$gentei_body_style","$gentei_siasenbako");

	print <<"EOM";
	<table  border="0" cellspacing="0" cellpadding="5" align=center >
	<tr>$centents_botan<td align=right>$saisenbako_data</td></tr>
	</table>
EOM

	print <<"EOM";
	<table width="$gentei_tablewidth" border="0" cellspacing="0" cellpadding="8" align=center style="$gentei_table2_style">
	<tr><td>
	<div style = "$gentei_title_style">$gentei_title</div>
	<div style = "$gentei_leed_style">$gentei_come</div>
	</td></tr>
	<td>
EOM
	$page=$in{'page'};	
	if ($page eq "") { $page = 0; }
	$i=0;
	$gentei_log_file = "./member/$in{'ori_ie_id'}/gentei_log.cgi";
	open(IN,"< $gentei_log_file") || &error("Open Error : $gentei_log_file");
	eval{ flock (IN, 1); };
	@bbs_alldata=<IN>;
	foreach (@bbs_alldata){
		($b_num,$b_name,$b_date,$b_title,$b_mail,$b_com,$b_id)= split(/<>/);#koko2006/12/11
		$i++;
		if ($i < $page + 1) { next; }
		if ($i > $page + $gentei_kensuu) { last; }
				print "<div style=\"$gentei_daimei_style\">$b_title</div><div>$b_com（$b_date）<span style=\"font-size:10px\">記事no.$b_num</span></div><br>\n";		#ver.1.40
	}		#foreach閉じ
	close(IN);
	
		$next = $page + $gentei_kensuu;
		$back = $page - $gentei_kensuu;
		print "<div align=center><table border=0><tr>";
		if ($back >= 0) {
			print <<"EOM";
	<td><form method="POST" action="$this_script">
	<input type=hidden name=mode value="houmon">
	<input type=hidden name=con_sele value="3">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
	<input type=hidden name=page value="$back">
	<input type=submit value="BACK"></form></td>
EOM
		}
		if ($next < $i) {
			print <<"EOM";
	<td><form method="POST" action="$this_script">
	<input type=hidden name=mode value="houmon">
	<input type=hidden name=con_sele value="3">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
	<input type=hidden name=page value="$next">
	<input type=submit value="NEXT"></form></td>
EOM
		}

	print <<"EOM";
	</tr></table></div>
	</td></tr>
	</table>
	<div align=center>
	<form method="POST" action="$this_script">
	<div style=" font-size: 10px; color: #444444"><br>
	<input type=hidden name=mode value="gentei_delete">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
	記事no. <input type=text name=b_num size=8>
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="削除">
	</form>
	※記事を書いた本人とゲーム管理者のみ「記事no.」を指定して記事を削除することができます。<br>
	</div>
EOM
	&hooter("login_view","家を出る");
exit;
}


#家主掲示板投稿処理
sub gentei_regist {
	&lock;
#ログファイル更新
	# ログを読み込み
	$gentei_log_file = "./member/$in{'iesettei_id'}/gentei_log.cgi";		#ver.1.3
	open(IN,"< $gentei_log_file") || &error("Open Error : $gentei_log_file");
	eval{ flock (IN, 1); };
	# 先頭行を取得
	$top = <IN>;
	local($b_num,$b_name,$b_date,$b_title,$b_mail,$b_come,$b_id)= split(/<>/, $top);#koko2006/12/11
#タグ禁止処理
	if ($in{'name'} eq $b_name && $in{'b_come'} eq $b_come) {
		&error("二重投稿です");
	}
	if ($in{'b_come'} eq "") {
		&error("内容が入力されていません");
	}
	# 新記事Noを取得
	$b_num++;
	# 更新配列を定義
	&time_get;
	$new[0] = "$b_num<>$in{'name'}<>$date2<>$in{'b_title'}<>$in{'b_mail'}<>$in{'b_come'}<>$in{'k_id'}<>\n"; #koko2006/12/11
	$new[1] = $top;

	while (<IN>) {
		$i++;
		push(@new,$_);
		if ($i >= 50){last;}
	}
	close(IN);

# ログを更新
	open(OUT,">$gentei_log_file") || &error("Write Error : $gentei_log_file");
	eval{ flock (OUT, 2); };
	print OUT @new;
	close(OUT);
# ロック解除
	&unlock;
	&message("投稿しました。","my_house_settei","original_house.cgi");
}

#####お店
sub omise {	
	$omise_log_file = "./member/$in{'ori_ie_id'}/omise_log.cgi";
	open(IN,"< $omise_log_file") || &error("Open Error : $omise_log_file");
	eval{ flock (IN, 1); };
	@omise_alldata=<IN>;
	close(IN);
#koko2007/10/26 場所移動
	if(!$k_id){&error("mono.cgi エラー original_hause1")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(MK,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (MK, 1); };
	@my_kounyuu_list =<MK>;
	close(MK);
#所有物チェックkoko2007/11/04場所移動追加
	foreach (@my_kounyuu_list){
		&syouhin_sprit ($_);
		if ($syo_kouka eq "クレジット"){
			if ($syo_taikyuu - (int ((time - $syo_kounyuubi) / (60*60*24)))){
				$siharai_houhou .= "<option value=\"$syo_hinmoku\">$syo_hinmoku</option>";
			}
		}

#koko2007/11/04
		if($kyokahin1 && $syo_hinmoku eq $kyokahin1 || $kyokahin2 && $syo_hinmoku eq $kyokahin2){ #koko2007/10/09
			$kyokasuru = 1;
		}elsif($kyokasuru != 1 && ($kyokahin1 || $kyokahin2)){
			$kyokasuru = 2;
		}
#end2007/11/04
	}

#種別でソートkoko2006/03/12
#				foreach (@omise_alldata){
#						$data=$_;
#						$key=(split(/<>/,$data))[0];
#						push @tinretu_alldata,$data;
#						push @keys,$key;
#				}
		@tinretu_alldata = @omise_alldata;
		@keys0 = map {(split /<>/)[0]} @tinretu_alldata;
	#	@alldata = @tinretu_alldata[sort {@keys0[$a] cmp @keys0[$b]} 0 .. $#keys0]; #変更ミス
		@tinretu_alldata = @tinretu_alldata[sort {@keys0[$a] cmp @keys0[$b]} 0 .. $#keys0]; #koko2006/08/21

#				sub by_syu_keys{$keys[$a] cmp $keys[$b];}
#				@tinretu_alldata=@tinretu_alldata[ sort by_syu_keys 0..$#tinretu_alldata]; 
#kokoend2006/03/12	
	$omise_settei_file = "./member/$in{'ori_ie_id'}/omise_ini.cgi";
		open(OIB,"< $omise_settei_file") || &error("Open Error : $omise_settei_file");
		eval{ flock (OIB, 1); };
			$omise_settei_data = <OIB>;
			($omise_title,$omise_come,$omise_body_style,$omise_syubetu,$omise_table1_style,$omise_table2_style,$omise_koumokumei,$omise_syouhin_table,$omise_title_style,$omise_leed_style,$omise_siasenbako,$omise_yobi5,$omise_yobi6,$omise_yobi7,$omise_yobi8,$omise_yobi9,$omise_yobi10)= split(/<>/,$omise_settei_data);
#omise_yobi5＝基本販売掛け率　omise_yobi6＝商品カテゴリーのスタイル設定　omise_yobi7＝リンクのスタイル
		close(OIB);
	&ori_header("$omise_body_style","$omise_siasenbako","$omise_yobi7");
		print <<"EOM";
	<table  border="0" cellspacing="0" cellpadding="5" align=center >
	<tr>$centents_botan<td align=right>$saisenbako_data</td></tr>
	</table>
EOM
	print <<"EOM";
	<form method="POST" action="$script">
	<input type=hidden name=mode value="buy_syouhin">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=yakub value="$in{'yakub'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
	<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center style="$omise_table1_style">
	<tr>
	<td  style="$omise_title_style" nowrap>$omise_title</td>
	<td style="$omise_leed_style" width=65%>$omise_come</td>
	</tr></table><br>
	<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center style="$omise_table2_style">
	<tr><td colspan=26>凡例：(国)＝国語up値、(数)＝数学up値、(理)＝理科up値、(社)＝社会up値、(英)＝英語up値、(音)＝音楽up値、(美)＝美術up値、（ル）=ルックスup値、（体）=体力up値、（健）=健康up値、（ス）=スピードup値、（パ）=パワーup値、（腕）=腕力up値、（脚）=脚力up値、（L）=LOVEup値、（面）=面白さup値、（H）=エッチup値<br>
	※ギフトは贈り物専用の商品です。自分で使用することはできません。
EOM
	if ($kaenai_seigen == 1){		#ver.1.40
		if ($k_id eq "$in{'ori_ie_id'}" || $house_type eq "$in{'ori_ie_id'}"){		#ver.1.3
			print "<br><font color=#ff6600>※自分や配偶者のお店で商品を買うことはできません。</font>";
		}
	}

	foreach (@tinretu_alldata) {
			&syouhin_sprit($_);
			if($syo_zaiko <= 0){next;}
#独自価格の設定があればその価格
			if ($tokubai){
					$syo_nedan = "$tokubai";
			}else{
				if ($omise_syubetu eq "スーパー"){
					$syo_nedan = int($syo_nedan *1.5 * $omise_yobi5);
				}else{
					$syo_nedan = int ($syo_nedan * $omise_yobi5);
				}
			}
			if($syo_zaiko <= 0){
					$kounyuubotan ="";
					$syo_zaiko = "売り切れ";
			}else{
					$kounyuubotan ="<input type=radio value=\"$syo_hinmoku,&,$syo_taikyuu,&,$syo_nedan,&,$syo_syubetu,&,\" name=\"syo_hinmoku\">"; #koko2006/08/22
			}
			if($syo_cal > 0){$calory_hyouzi = "$syo_cal kcal";}else{$calory_hyouzi = "ー";}
			if ($maeno_syo_syubetu ne "$syo_syubetu"){
			   print <<"EOM";
			   <tr style="$omise_yobi6"><td align=center nowrap>▼$syo_syubetu</td><td align=center>価格</td><td align=center nowrap>在庫</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center nowrap>カロリー</td><td align=center nowrap>耐久</td><td align=center>使用<br>間隔</td><td align=center>身体<br>消費</td><td align=center>頭脳<br>消費</td></tr>
EOM
			}
			$taikyuu_hyouzi_seikei = "$syo_taikyuu"."$syo_taikyuu_tani";
#ver.1.3ここから
if ($syo_nedan =~ /^[-+]?\d\d\d\d+/g) {
  for ($i = pos($syo_nedan) - 3, $j = $syo_nedan =~ /^[-+]/; $i > $j; $i -= 3) {
    substr($syo_nedan, $i, 0) = ',';
  }
}
#ver.1.3ここまで
#koko2006/11/06 #koko2006/11/07
	if ($syo_comment){
		$disp_seru = "rowspan=\"2\"";
		$disp_com = "<tr><td align=left colspan=24>【 備考 】 $syo_comment</td></tr>"; #koko2006/11/07
	}else{
		$disp_seru = "";
		$disp_com = "";
	}
#koko2007/10/09
		$mottru = 0;#koko2007/10/26
		foreach $tempo(@my_kounyuu_list){
			(@temporari) = split(/<>/,$tempo);
			if($syo_syubetu eq $temporari[0] && $syo_hinmoku eq $temporari[1]){
				if ($temporari[22] eq "日"){
					$keikanissuu = int ((time - $temporari[30]) / (60*60*24));
					$mottru = $temporari[21] - $keikanissuu;
				}else{
					$nokori = int($temporari[21]/$syo_taikyuu);
					if($temporari[21]%$syo_taikyuu){$mottru = $nokori+1;}else{$mottru = $nokori;}
				}
				last;
			}
		}
#koko2007/11/04
		if($kyokasuru == 2 || $kyokasuru == 1){
			$fukyoka = 0;
			foreach $temp0 (@kyokahitsuyou){
				if($syo_hinmoku eq $temp0){
					$fukyoka = 1;
				}
			}
		}

		if($fukyoka == 1 && $mottru && $kyokasuru == 1){
			$in_hinmoku = "$kounyuubotan <font color=\"ff00ff\">$syo_hinmoku($mottru)</font>";
		}elsif($fukyoka == 1 && $mottru){
			$in_hinmoku = "<font color=\"ff00ff\">$syo_hinmoku($mottru)</font>";
		}elsif($fukyoka == 1 && $kyokasuru == 1){
			$in_hinmoku = "$kounyuubotan <font color=\"ff0000\">$syo_hinmoku</font>";
		}elsif($fukyoka == 1){
			$in_hinmoku = "<font color=\"ff0000\">$syo_hinmoku</font>"; #end2007/11/04
		}elsif($mottru){
			$in_hinmoku = "$kounyuubotan <font color=\"0000ff\">$syo_hinmoku($mottru)</font>";
		}else{
			$in_hinmoku = "$kounyuubotan $syo_hinmoku";
		}#end2007/10/26

		print <<"EOM";
		<tr style="$omise_syouhin_table" align=center><td nowrap align=left $disp_seru>$in_hinmoku</td><td align=right nowrap>$syo_nedan円</td><td align=right>$syo_zaiko</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right nowrap>$calory_hyouzi</td><td nowrap>$taikyuu_hyouzi_seikei</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td></tr>$disp_com
EOM
#kokoend　end2007/10/26

		$maeno_syo_syubetu = "$syo_syubetu";
	}		#foreach閉じ
#ver.1.30ここから
	print <<"EOM";
	<tr><td colspan=26><div align=center>
	支払い方法 <select name="siharaihouhou"><option value="現金">現金</option>$siharai_houhou</select>
	個数 <select name="kosuu">
EOM
for ($i=1 ; $i<=$item_kosuuseigen ; $i++){ 
			print "<option value=\"$i\">$i個</option> \n";
}
	print <<"EOM";
</select>
	<input type=submit value=" O K "></div></td></tr>
	</table></form>
	<div align="center"><a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div>
EOM
#ver1.30ここまで
	&hooter("login_view","家を出る");
	exit;
}


#####独自URL
sub dokuzi_url {
	$dokuzi_settei_file = "./member/$in{'ori_ie_id'}/dokuzi_ini.cgi";
		open(OIB,"< $dokuzi_settei_file") || &error("Open Error : $dokuzi_settei_file");
		eval{ flock (OIB, 1); };
			$dokuzi_settei_data = <OIB>;
			($dokuzi_url,$dokuzi_width,$dokuzi_height,$dokuzi_haikei_style,$dokuzi_title,$dokuzi_come,$dokuzi_title_style,$dokuzi_leed_style,$dokuzi_siasenbako,$dokuzi_yobi10) = split(/<>/,$dokuzi_settei_data);
		close(OIB);
	&ori_header("$dokuzi_haikei_style","$dokuzi_siasenbako");
	print <<"EOM";
	<table  border="0" cellspacing="0" cellpadding="5" align=center >
	<tr>$centents_botan<td align=right>$saisenbako_data</td></tr>
	</table>
EOM
	print <<"EOM";
	<table width="$dokuzi_tablewidth" border="0" cellspacing="0" cellpadding="8" align=center style="$dokuzi_table2_style">
	<tr><td>
	<div style = "$dokuzi_title_style">$dokuzi_title</div>
	<div style = "$dokuzi_leed_style">$dokuzi_come</div>
	</td></tr>
	<tr><td align=center>
	<IFRAME src="$dokuzi_url"  width="$dokuzi_width" height="$dokuzi_height" scrolling=auto marginheight=0 FRAMEBORDER=0></IFRAME>
	</td></tr>
	</table></body></html>
EOM
	&hooter("login_view","家を出る");
exit;
}

###さい銭箱入金処理
sub saisensuru {		#ver.1.3
	if ($money < $in{'saisengaku'}){&error("お金が足りません。");}
#koko2005/09/01
	if ($in{'saisengaku'} < 0){&error("マイナス額は取り扱い出来ません。");}
	&osaisen_chc_aite; #koko2005/05/05 新規

	$money -= $in{'saisengaku'};
#ログ更新
	&lock;	
			&temp_routin;
			open(OUT,">$my_log_file") || &error("$my_log_fileに書き込めません");
			eval{ flock (OUT, 2); };
			print OUT $k_temp;
			close(OUT);

	&openAitelog ($in{'ori_ie_id'});
	$aite_bank += $in{'saisengaku'};
	
			&aite_temp_routin;
				open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
				eval{ flock (OUT, 2); };
				print OUT $aite_k_temp;
				close(OUT);
#ver.1.40ここまで
	&aite_kityou_syori("おさい銭←$name","",$in{'saisengaku'},$aite_bank,"普",$in{'ori_ie_id'},"lock_off");
	&unlock;
	&header("","sonomati");
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
	$aite_nameさんに$in{'saisengaku'}円のおさい銭をしました。
	</td></tr></table>
	<br><br><a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div>
	</body></html>
EOM
exit;
}

######通帳チェック koko 2005/05/05
sub osaisen_chc_aite {
	my (@aite_tuutyou);
	$ginkoumeisai_file="./member/$in{'ori_ie_id'}/ginkoumeisai.cgi";
	open(GM,"< $ginkoumeisai_file") || &error("相手の預金通帳ファイルが開けません");
	eval{ flock (GM, 1); };
	@aite_tuutyou = <GM>;
	close(GM);

	&time_get; #$date

	foreach (@aite_tuutyou) {
		my ($tu_date,$meisai,$soukingaku,$nyukigaku) = split(/<>/);
		if ($tu_date eq $date && $meisai eq "おさい銭←$name"){
			$kojinbetu_osaisen += $nyukigaku;
			if ($kojinbetu_osaisen + $in{'saisengaku'} > $osaisenjyougen){
				&error("今日、この人へのお賽銭が上限を超します。<br>おさい銭出来ません。");
			}

		}
		if ($tu_date eq $date && ($meisai =~ /おさい銭←./)){
			$total_osaisen += $nyukigaku;
			if ($total_osaisen + $in{'saisengaku'} > $totalosaisenjyougen){
				&error("今日、この人はお賽銭を十\分もらってます。<br>あしたおさい銭してね。");
			}

		}

	}

}



##########自分のお店の商品リスト
sub my_syouhin {
	$omise_log_file="./member/$in{'iesettei_id'}/omise_log.cgi";
	open(SP,"< $omise_log_file") || &error("Open Error : $omise_log_file");
	eval{ flock (SP, 1); };
	@myitem_hairetu = <SP>;
	close(SP);
#価格変更の場合
	if ($in{'command'} eq "価格設定"){
		if ($in{'syo_nedan'} * 3 < $in{'hanbaikakaku'}){&error("販売価格は仕入れ価格の３倍以内にしてください。");}
		if ($in{'syo_nedan'} / 10 > $in{'hanbaikakaku'}){&error("販売価格は仕入れ価格の10分の1以上にしてください。");}
		if($in{'hanbaikakaku'} =~ /[^0-9]/){&error("販売価格が不適切です。");}			#ver.1.3
		@new_myitem_hairetu =(); #koko2007/06/05
		foreach  (@myitem_hairetu) {
			&syouhin_sprit($_);
			if ($in{'syo_hinmoku'} eq "$syo_hinmoku"){
					$tokubai = $in{'hanbaikakaku'};
					$syo_comment = $in{'bikou'}; #koko2007/09/27
			}
			&syouhin_temp;
			push (@new_myitem_hairetu,$syo_temp);
		}
		&lock;
		open(OUT,">$omise_log_file") || &error("Write Error : $omise_log_file");
		eval{ flock (OUT, 2); };
		print OUT @new_myitem_hairetu;
		close(OUT);	
		&unlock;
		&message("$in{'syo_hinmoku'} の価格を$in{'hanbaikakaku'}円に設定しました。<br>備考を「$in{'bikou'}」にしました。","my_syouhin","original_house.cgi");#koko2007/09/27
	}
	
#種別でソート
#koko2006/03/12
				@alldata = @myitem_hairetu;
#				foreach (@myitem_hairetu){
#						$data=$_;
#						$key=(split(/<>/,$data))[0];
#						push @alldata,$data;
#						push @keys,$key;
#				}

				@keys0 = map {(split /<>/)[0]} @myitem_hairetu;
				@alldata = @alldata[sort {@keys0[$a] cmp @keys0[$b]} 0 .. $#keys0];


#				sub by_syu_keys{$keys[$a] cmp $keys[$b];}
#				@alldata=@alldata[ sort by_syu_keys 0..$#alldata]; 
#kokomade

#お店設定ファイルより販売掛け率を取得
	$omise_settei_file = "./member/$in{'iesettei_id'}/omise_ini.cgi";
		open(OIB,"< $omise_settei_file") || &error("Open Error : $omise_settei_file");
		eval{ flock (OIB, 1); };
			$omise_settei_data = <OIB>;
			($omise_title,$omise_come,$omise_body_style,$omise_syubetu,$omise_table1_style,$omise_table2_style,$omise_koumokumei,$omise_syouhin_table,$omise_title_style,$omise_leed_style,$omise_siasenbako,$omise_yobi5,$omise_yobi6,$omise_yobi7,$omise_yobi8,$omise_yobi9,$omise_yobi10)= split(/<>/,$omise_settei_data);
		close(OIB);
		
	&header(omise_list_style);
	print <<"EOM";
	<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>各商品の販売価格はこちらで個別に設定することができます。ただし、仕入れ価格の３倍以上に設定することはできません。<br>
	現在のお店の種類 = $omise_syubetu</td>
	</tr></table><br>
	
	<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr><td colspan=28><font color=#330033>凡例：(国)＝国語up値、(数)＝数学up値、(理)＝理科up値、(社)＝社会up値、(英)＝英語up値、(音)＝音楽up値、(美)＝美術up値、（ル）=ルックスup値、（体）=体力up値、（健）=健康up値、（ス）=スピードup値、（パ）=パワーup値、（腕）=腕力up値、（脚）=脚力up値、（L）=LOVEup値、（面）=面白さup値、（H）=エッチup値<br>
	※耐久は、○回なら使用できる回数、○日なら使用できる日数です。<br>
	※カロリーは摂取できる数値です。</font></td></tr>
		<tr bgcolor=#996699><td align=center nowrap>商品</td><td align=center nowrap>販売価格</td><td align=center nowrap>仕入れ価格</td><td align=center nowrap>在庫</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center nowrap>カロリー</td><td align=center>使用<br>間隔</td><td align=center nowrap>身体<br>消費</td><td align=center nowrap>頭脳<br>消費</td><td align=center nowrap>耐久</td><td align=center nowrap>購入日</td></tr>
EOM

	foreach (@alldata) {
			&syouhin_sprit($_);
			if ($omise_syubetu ne "スーパー"){
				if ($omise_syubetu ne "$syo_syubetu"){next;}
			}
			if($syo_cal > 0){$calory_hyouzi = "$syo_cal kcal";}else{$calory_hyouzi = "<div align=center>ー</div>";}
			if ($maeno_syo_syubetu ne "$syo_syubetu"){
				print "<tr bgcolor=#cc9999><td colspan=28>▼$syo_syubetu</td></tr>";
			}
			$taikyuu_hyouzi_seikei = "$syo_taikyuu"."$syo_taikyuu_tani";
			&byou_hiduke($syo_kounyuubi);
			if ($omise_syubetu eq "スーパー"){
				$syo_nedan *= 1.5;
			}
#独自の価格設定をしている場合その価格、そうでなければ設定の掛け率
			if ($tokubai){$hannbaityuu = "$tokubai";}else{$hannbaityuu = $syo_nedan * $omise_yobi5;}

		print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="my_syouhin">
	<input type=hidden name=command value="価格設定">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name=syo_hinmoku value="$syo_hinmoku">
	<input type=hidden name=syo_nedan value="$syo_nedan">
		<tr bgcolor="#ffcccc" align="center"><td nowrap align=left>$syo_hinmoku<input type=submit value="OK"></td><td nowrap><input type="text" name="hanbaikakaku" size=8 value=$hannbaityuu><td nowrap align=right>$syo_nedan</td></td><td nowrap>$syo_zaiko</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right>$calory_hyouzi</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td><td nowrap>$taikyuu_hyouzi_seikei</td><td nowrap>$bh_tukihi</td></tr><tr bgcolor=#cccccc><td align=left colspan=27><input type="text" name="bikou" size=80 value=$syo_comment>$syo_comment<br></td></form></tr>
EOM
		$maeno_syo_syubetu = "$syo_syubetu";
	}		#foreach閉じ
	if (! @alldata){print "<tr><td colspan=26>現在所有しているアイテムはありません。</td></tr>";}
	print <<"EOM";
	</table>
EOM
	&hooter("my_house_settei","戻る","original_house.cgi");
	exit;
}

###BBS記事削除
sub bbs_delete {
	if ($in{'b_count'} eq "" && $in{'oya_count'} eq "" && !$in{'all_del'}){&error("記事no.が指定されていません");} #koko2007/09/17
	&lock;
#ログファイル更新
	# ログを読み込み
	if ($in{'ori_ie_id'} eq "admin"){
		$bbs1_log_file = "./member/admin/bbs".$in{'bbs_num'}."_log.cgi";
	}else{
		$bbs1_log_file = "./member/$in{'ori_ie_id'}/bbs1_log.cgi";
	}
	open(IN,"< $bbs1_log_file") || &error("Open Error : $bbs1_log_file");
	eval{ flock (IN, 1); };
	$count_gyou = <IN>;
	@all_data = <IN>;
	close(IN);
	$kizi_atta_flag = 0;
	$sakujo_b_num = "";
	@new_all_data = ();
	$i=0;
	foreach $tep_dat(@all_data){
		($b_num,$b_name,$b_date,$b_res,$b_mail,$b_com,$b_id)= split(/<>/, $tep_dat);#koko2006/12/11
		if ($in{'b_count'} eq "$b_mail"){
			$kizi_atta_flag = 1;
			if ($b_num){$sakujo_b_num = "$b_num";}else{$sakujo_b_num = "res";}
			$b_name =~ s/<span style="font-size:10px">（.*//;
			if (!($in{'name'} eq $admin_name || $in{'ori_ie_id'} eq $k_id)){ #koko2006/11/25
				&error("管理者以外は記事削除できません。");
			}else{
				$tep_dat = "";#koko2007/04/19
				next;
			}
		}

#koko2007/09/17
		if (!($in{'name'} eq $admin_name || $in{'ori_ie_id'} eq $k_id)){ #koko2006/11/25
			&error("管理者以外は記事削除できません。");
		}else{
			if ($in{'oya_count'}){
				if($delettyu && $b_num){
					$delettyu = 0;
				}
				if($b_num eq $in{'oya_count'}){
					$kizi_atta_flag = 1;
					$delettyu = 1;
					next;
				}
			}
		}
#kokoend


		if ($b_res){if ($b_res eq "$sakujo_b_num"){&error("子記事のついた親記事は削除できません。");}}
	#	$bbs_temp = "$b_num<>$b_name<>$b_date<>$b_res<>$b_mail<>$b_com<>$b_id<>\n"; #koko2006/12/14

		push (@new_all_data,$tep_dat);#koko2007/04/19
	#	push (@new_all_data,$bbs_temp);
	}
#koko2007/09/17
	if (!($in{'name'} eq $admin_name || $in{'ori_ie_id'} eq $k_id)){ #koko2006/11/25
		&error("管理者以外は記事削除できません。");
	}else{
		if ($in{'all_del'}){
			$kizi_atta_flag = 1;
			@new_all_data = ();
		}
	}
	if ($kizi_atta_flag == 0){&error("該当する記事no.が見つかりません。");}
#	unshift (@new_all_data,$count_gyou);
	open (OUT,">$bbs1_log_file") || &error("Write Error : $bbs1_log_file");
	eval{ flock (OUT, 2); };
	print OUT $count_gyou;#koko2007/04/19
	print OUT @new_all_data;
	close(OUT);
	&unlock;
	&header("","sonomati");
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">記事を削除しました。1</span>
</td></tr></table>
<br>
	<form method=POST action="$this_script">
EOM
	if ($in{'ori_ie_id'} eq "admin"){
		print "<input type=hidden name=mode value=\"normal_bbs\">";
	}else{
		print "<input type=hidden name=mode value=\"houmon\">";
	}
	print <<"EOM";
	<input type=hidden name=con_sele value="0">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
	<input type=hidden name=bbs_num value="$in{'bbs_num'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="戻る">
	</form></div>
EOM
	exit;
}

###家主限定掲示板記事削除
sub gentei_delete {
	if ($in{'ori_ie_id'} != $k_id and $in{'ori_ie_id'} != $house_type and $in{'name'} ne $admin_name){&error("家主（配偶者）、ゲーム管理者以外は記事削除できません。");}
	if ($in{'b_num'} eq ""){&error("記事no.が指定されていません");}
	&lock;
#ログファイル更新
	# ログを読み込み
	$gentei_log_file = "./member/$in{'ori_ie_id'}/gentei_log.cgi";
	open(IN,"< $gentei_log_file") || &error("Open Error : $gentei_log_file");
	eval{ flock (IN, 1); };
	@all_data=<IN>;
	close(IN);
	$kizi_atta_flag = 0;
	@new_all_data = ();
	foreach $tep_dat(@all_data){
		($b_num,$b_name,$b_date,$b_title,$b_mail,$b_com,$b_id)= split(/<>/, $tep_dat);#koko2006/12/11
		if ($in{'b_num'} eq "$b_num"){
			$kizi_atta_flag = 1;
			if ($name ne $b_name &&  $in{'name'} ne $admin_name){&error("書いた本人以外は記事削除できません。");
			}else{
				$tep_dat = "";#koko2007/04/19
				next;
			}
		}
	#	$bbs_temp = "$b_num<>$b_name<>$b_date<>$b_title<>$b_mail<>$b_com<>$in{'k_id'}<>\n"; #koko2006/12/11
		push (@new_all_data,$tep_dat);#koko2007/04/19
	#	push (@new_all_data,$bbs_temp);
	}
	if ($kizi_atta_flag == 0){&error("該当する記事no.が見つかりません。");}
	open (OUT,">$gentei_log_file") || &error("Write Error : $gentei_log_file");
	eval{ flock (OUT, 2); };
	print OUT @new_all_data;
	close(OUT);
	&unlock;
	&header("","sonomati");
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">記事を削除しました。2</span>
</td></tr></table>
<br>
	<form method=POST action="$this_script">
	<input type=hidden name=mode value="houmon">
	<input type=hidden name=con_sele value="3">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
	<input type=hidden name=bbs_num value="$in{'bbs_num'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="戻る">
	</form></div>
EOM
	exit;
}