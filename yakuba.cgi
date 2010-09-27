#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
#############################
# 役場のみのcgi
# 2007/11/
############################

$this_script = 'yakuba.cgi';
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
if($in{'mode'} eq "yakuba"){&yakuba;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;

#######ランキング表示
sub yakuba {
	$hausu_disp = 1;
	&lock;
	$now_time= time;
	if($in{'sortid'}){$sortid = $in{'sortid'};}else{$sortid = 5;}
	
	open(IN,"< $logfile") || &error("Open Error : $logfile");
	eval{ flock (IN, 1); };
	@rankingMember = <IN>;
	close(IN);
	@alldata = ();
	foreach (@rankingMember) {
		&list_sprit($_);
		#放置ユーザー削除処理
		$now_time = time;
		$tatta = int(($now_time - $list_first_access) / (24 * 60 * 60));
        
		if($list_last_syokuzi < $now_time - (60*60*24*$deleteUser)){
			#家削除処理
			&ie_sakujo_syori ($list_name);
			#アンケート削除処理
			&enq_sakujo_syori ($list_name);
			#結婚削除処理
			&kekkon_sakujo($list_name);
			#プロフィール＆結婚斡旋所削除処理
			&prof_sakujo2 ($list_name);
			&as_prof_sakujo2($list_name);
			
			#フォルダー内のファイル名を取得して削除。個人フォルダーの削除
			$sakujo_folder_id = "./member/$list_k_id";
			if (-e "$sakujo_folder_id") {
				use DirHandle;
				$dir = new DirHandle ("./member/"."$list_k_id");
				while($file_name = $dir->read){
					unlink ("./member/$list_k_id/$file_name");
				}
				$dir->close;
				rmdir("./member/$list_k_id") || &error("ID番号$list_k_idの$list_nameさんのデータ削除ができません");
			}
			&news_kiroku("転居","$list_nameさんが街を去りました。");
            
			next;
		}
		$data=$_;
        
		push @alldata,$data;
	}
    
	if ($mem_lock_num == 0){
		$err = &data_save($logfile, @alldata);
		if ($err) {&error("$err");}
	}else{
		open(OUT,">$logfile") || &error("$logfileが開けません");
		eval{ flock (OUT, 2); };
		print OUT @alldata;
		close(OUT);
	}
    
	&unlock;
	
	@keys0 = map {(split /<>/)[$in{'sortid'}]} @alldata;
	@alldata = @alldata[sort {@keys0[$b] <=> @keys0[$a]} 0 .. $#keys0];
    
	($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($first_access);
	$mon  = $mon+1;
	$year = $year + 1900;
	$in_data = "$year年$mon月$mday日  $hour時$min分";
	$now_time = time;
	$tatta=int(($now_time-$first_access) / (24*60*60));

	&header(yakuba_style);
	print <<"EOM";
	<table width="98%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>役場では新規入居者や各種ランキングを見ることができます。<br>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="yakuba">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value=$in{'town_no'}>
	<select name="sortid">
    
	<option value="">最近の街のニュース$news_kensuu件</option>
EOM

	print "<option value=23";
	if ($sortid == 23){print " selected";}
	print ">最近の入居者$rankMax人</option>";
		
	 print "<option value=52";
	 if ($sortid == 52){print " selected";}
	 print ">Ｋポイントランキングベスト$rankMax</option>";
	 
	 print "<option value=43";
	 if ($sortid == 43){print " selected";}
	 print ">仕事経験値ランキングベスト$rankMax</option>";

	print "<option value=49";
	if ($sortid == 49){print " selected";}
	print ">長者番付ベスト$rankMax</option>";
	
	@global_nouryokuti = ("国語","数学","理科","社会","英語","音楽","美術","ルックス","体力","健康","スピード","パワー","腕力","脚力","LOVE","面白さ","エッチ");
	$i=6;
	foreach (@global_nouryokuti) {
		print "<option value=$i";
		if ($sortid == $i){print " selected";}
		print ">$_ランキングベスト$rankMax</option>";
		$i ++;
	}

	if($in{'name'} eq $admin_name){
		$kanrisya_disp = "<option value=kanrinin>イベント全体</option>\n";
	}
	
	print <<"EOM";
<option value=jyu>住所録</option>
<option value=iu>発言</option>
<option value=ev>個人イベント</option>
$kanrisya_disp
</select> <input type=submit value="OK">
<select name="omise"><option value="">すべて</option>
EOM

	foreach (@global_syouhin_syubetu){
		print "<option value=$_";
		if ($in{'omise'} eq "$_"){print " selected";}
		print ">$_</option>\n";
	}
    
	print <<"EOM";
</select>
</form>
$nameさんが、$titleに来たのは$in_data<BR>$tatta日経ちました<BR>
</td>
<td bgcolor="#333333" align=center width=300><font color="#ffffff" size="5"><b>役　場</b></font></td>
</tr></table><br>
EOM

	if($in{'sortid'} eq "jyu"){

		open(IN,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
		eval{ flock (IN, 1); };
		@ori_ie_para = <IN>;
		close(IN);
		@jyusyo=();
        
		$i=0;
		$nijyuu = 0;
		foreach (@ori_ie_para){
			if ($_ eq $ori_ie_para[0] && $i){
				$nijyuu = $i;
			#	&error("二重書き込み adm 1");
				last;
			}
			$i++;
		}
		if ($nijyuu){
			splice @ori_ie_para,$nijyuu;
			open(OUT,">$ori_ie_list") || &error("Open Error : $ori_ie_list");
			eval{ flock (OUT, 2); };
			print  OUT @ori_ie_para;
			close(IN);
		}
#kokoend
#koko2007/03/19
	#	open(OI,"< $ori_ie_list") || &error("Open Error : $ori_ie_list"); #koko2007/05/09
	#	@ori_ie_hairetu = <OI>;
#koko2008/02/17



#end2008/02/17
		foreach (@ori_ie_para) { #foreach (@ori_ie_hairetu) {
			&ori_ie_sprit($_);
			$unit{"$ori_k_id"} = "<img src=\"$ori_ie_image\">";	#ver.1.40 #koko2006/12/13 #koko2007/04/27 #koko2007/09/17
		}
	#	close(OI);
#kokoend2007/03/19
		@tata=('A','B','C','D','E','F','G','H','I','J','K','L');

		foreach (@ori_ie_para){
			&ori_ie_sprit($_);
			$z=int(($ori_ie_tateziku-21) / 16);
			if ($in{'omise'}){
#koko2008/02/17
			if($ori_ie_syubetu eq $in{'omise'}){
				$jyusyo[$ori_ie_town].="<TR><TD>$ori_ie_name</TD><TD>$unit{\"$ori_k_id\"}</TD><TD nowrap>$tata[$z]-$ori_ie_yokoziku<br>$ori_ie_syubetu</TD><TD>$ori_ie_setumei</TD></TR>\n"; #koko2007/03/17 #koko2007/03/19
				}
			}else{
				$jyusyo[$ori_ie_town].="<TR><TD>$ori_ie_name</TD><TD>$unit{\"$ori_k_id\"}</TD><TD nowrap>$tata[$z]-$ori_ie_yokoziku<br>$ori_ie_syubetu</TD><TD>$ori_ie_setumei</TD></TR>\n"; #koko2007/03/17 #koko2007/03/19
			}
#kokoend
		}
#個人の家情報をunitハッシュに代入
		print "<table border=\"1\" cellspacing=\"0\" cellpadding=\"5\" align=center class=yosumi bgcolor=#eeeecc><tr><TD ALIGN=left VALIGN=top width=100%>\n"; #koko2007/03/24

		$i = 0;
		foreach (@town_hairetu){ #town_ini.cgi にて設定されている。
			if($machikakushi eq 'yes'){#koko2007/10/21
				unless(($i == $kakushimachi_no && $kakushimachi_no) || ($i == $kakushimachi_no1 && $kakushimachi_no1) || ($i == $kakushimachi_no2 && $kakushimachi_no2) || ($i == $kakushimachi_no3 && $kakushimachi_no3) || ($i == $kakushimachi_no4 && $kakushimachi_no4)){ #koko2007/06/13  3 = ダウンタウン$kakushimachi_no3
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

#		print <<"EOM";
#		</table>
#EOM
#koko2007/10/27
	}elsif($in{'sortid'} eq "iu"){
		$aisatu_datfile = "./log_dir/aisatu_dat.cgi";
		open(IN,"< $aisatu_datfile") || &error("Open Error : $aisatu_detfile");
		eval{ flock (IN, 1); };
		@aisatu_data = <IN>;
		close(IN);
		$aru = 0;
		$ima_time = time;
		$i = 0;

		foreach (@aisatu_data) {
			($ai_id,$ai_name,$ai_kaisu,$ai_time) = split(/<>/);
			if($ai_time+30*24*60*60 < $ima_time){next;}
			if($ai_id){
				$iruka = "./member/$ai_id/log.cgi";
				if (! -e $iruka){next;}
			}
			push @new_aisatu_date,$_;
		}

		@iu_Keys = map {(split /<>/)[2]} @new_aisatu_date;
		@new_aisatu_date = @new_aisatu_date[sort {@iu_Keys[$b] <=> @iu_Keys[$a]} 0 .. $#iu_Keys];

		if($#new_aisatu_date+1 >= $rankMax){$#new_aisatu_date = $rankMax -1;}

		open(IN,"> $aisatu_datfile") || &error("Open Error : $aisatu_detfile");
		eval{ flock (IN, 2); };
		print IN @new_aisatu_date;
		close(IN);

		$i = 1;
		$ii = 0;
		$iii = 0;
		foreach (@new_aisatu_date) {
			($ai_id,$ai_name,$ai_kaisu,$ai_time) = split(/<>/);
			if($ii ne $ai_kaisu){$ii = $ai_kaisu;$iii = $i;}
			$i++ ;
			if(!$max_kaisu){$max_kaisu = $ai_kaisu;}
			$rank_a = int($max_kaisu / 3) * 2;
			$rank_b = int($max_kaisu / 3);
			if($ai_kaisu >= $rank_a && !$br1){$disp_dat .="ランクＡ<br>";$br1 = 1;}
			elsif($ai_kaisu >= $rank_b && $ai_kaisu < $rank_a && !$br2){$disp_dat .="<br>ランクＢ<br>";$br2 = 1;}
			elsif($ai_kaisu >=1 && $ai_kaisu < $rank_b && !$br3){$disp_dat .="<br>ランクＣ<br>";$br3 = 1;}
			$disp_dat .= "●$iii $ai_name($ai_kaisu) ";
		}

		open(OUT,"< $aisatu_logfile") || &error("Write Error : $aisatu_logfile");
		eval{ flock (OUT, 1); };
		@new_aisatu_date = <OUT>;
		close(OUT);

		foreach (@new_aisatu_date) {
			local($a_num,$a_name,$a_date,$a_com,$a_syurui,$ie_link,$jynken_mes)= split(/<>/);
			($in_time0,$in_time1) = split(/\ /,$a_date);
			$in_time = "$in_time0 $in_time1";
			if ($ie_link){
				$aisatu_table .= "<form method=POST action=\"original_house.cgi\" style=\"\margin-top: 0;margin-right: 0;margin-bottom: 0;margin-left: 0\"><input type=hidden name=mode value=houmon><input type=hidden name=name value=\"$in{'name'}\"><input type=hidden name=pass value=\"$in{'pass'}\"><input type=hidden name=k_id value=\"$in{'k_id'}\"><input type=hidden name=town_no value=\"$in{'town_no'}\">$ie_link<input type=image src=\"./img/house/house_mini.gif\"><span  style=\"color:$top_aisatu_hyouzi_iro1;\">$a_name ($a_syurui)：</span><span  style=\"color:$top_aisatu_hyouzi_iro2;\">$a_com $in_time</span></form>\n";
			}else{
				$aisatu_table .= "<span  style=\"color:$top_aisatu_hyouzi_iro1;\">$a_name ($a_syurui)：</span><span  style=\"color:$top_aisatu_hyouzi_iro2;\">$a_com $in_time</span><br>\n";
			}
		}

		print <<"EOM";
	<table width="98%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>$disp_dat</td><tr><td>$aisatu_table</td></tr>

EOM
	print "</table>";
	
	&hooter("login_view","戻る");
	exit;
    
	}elsif($in{'sortid'} eq "ev"){
		open(IN,"< $event_fail") || &error("$event_failが開けません。");
		eval{ flock (IN, 1); };
		@town_event = <IN>;
		close(IN);

		foreach (@town_event){
			($ev_time,$ev_name,$ev_event0) = split(/<>/);
			if($ev_name eq $in{'name'}){
				$disp_ev .= "<tr><td>$ev_name($ev_time)</td><td>$ev_event0</td></tr>\n";
			}
		}
		if($disp_ev eq ""){$disp_ev = "記録は残っていません。";}

		print <<"EOM";
<table width="98%" border="0" cellspacing="0" cellpadding="2" align=center class=yosumi>
<tr><td bgcolor=#ffffff><table>$disp_ev</table></td></tr></table>
EOM
		&hooter("login_view","戻る");
		exit;

	}elsif($in{'sortid'} eq "kanrinin"){
		open(IN,"< $event_fail") || &error("$event_failが開けません。");
		eval{ flock (IN, 1); };
		@town_event = <IN>;
		close(IN);

		print "<table width=\"98%\" border=\"0\" cellspacing=\"0\" cellpadding=\"2\" align=center class=yosumi><tr><td bgcolor=#ffffff>\n";
		print "<table>\n";
		foreach (@town_event){
			($ev_time,$ev_name,$ev_event0) = split(/<>/);
			print "<tr><td>$ev_name($ev_time)</td><td>$ev_event0</td></tr>\n";
		}
		if($#town_event == -1){print "イベント記録はありません。<br>\n";}
		print "</table></td></tr></table>\n";
		&hooter("login_view","戻る");
		exit;

	}elsif($in{'sortid'} eq ""){
#にゃんこタウン　kokoend
#koko2007/09/17
		$yakuba_aisatu = 'no';# 'yes';
		$time_stanpu = 'yes';

#街ニュース表示
				open(NS,"< $news_file") || &error("$news_fileが開けません。");
				eval{ flock (NS, 1); };
				@town_news = <NS>;
				close(NS);
					print <<"EOM";
					
					$aisatu_table
					

					<table width="98%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
					<tr bgcolor=#eeeecc><td>
					<div class=honbun4>◎最近の街のニュース$news_kensuu件</div>
EOM
				foreach (@town_news){
					my ($hiduke,$nw_syubetu,$nw_kizi)= split(/<>/);
					if ($nw_syubetu eq "恋人"){$news_style = "color:#ff3366;"; $news_kigou = "&#9829;";}
					elsif ($nw_syubetu eq "結婚"){$news_style = "color:#ff3300;"; $news_kigou = "&#9829;";}
					elsif ($nw_syubetu eq "入居"){$news_style = "color:#3366cc;"; $news_kigou = "◆";}
					elsif ($nw_syubetu eq "出産"){$news_style = "color:#009900;"; $news_kigou = "●";}
					elsif ($nw_syubetu eq "男出産"){$news_style = "color:#3366cc;"; $news_kigou = "♂ ";} #koko2007/11/25
					elsif ($nw_syubetu eq "女出産"){$news_style = "color:#ff3366;"; $news_kigou = "♀ ";} #koko2007/11/25
					elsif ($nw_syubetu eq "就職"){$news_style = "color:#009900;"; $news_kigou = "◎";}
					elsif ($nw_syubetu eq "別れ"){$news_style = "color:#666666;"; $news_kigou = "&#9829;";}
					elsif ($nw_syubetu eq "死亡"){$news_style = "color:#666666;"; $news_kigou = "■";}
					elsif ($nw_syubetu eq "転居"){$news_style = "color:#666666;"; $news_kigou = "▲";}
					elsif ($nw_syubetu eq "家"){$news_style = "color:#990000;"; $news_kigou = "●";}
					elsif ($nw_syubetu eq "地震"){$news_style = "color:#990000;"; $news_kigou = "×";} #koko2007/12/14
					elsif ($nw_syubetu eq "運用"){$news_style = "color:#990000;"; $news_kigou = "○";} #koko2007/12/14

					print <<"EOM";
					<div style="color:#666666; line-height:180%;">$hiduke<span style="$news_style"> $news_kigou$nw_kizi</span></div>
EOM
				}
				print "</td></tr></table><br><br>";
	}else{
	print <<"EOM";
    
<Script Language="JavaScript"><!--
	function Change(place){
		place.style.backgroundColor='#ff9900';
		place.style.color='#ffffff';
	}
	function Back(place){
		place.style.backgroundColor='';
		place.style.color='';
	}
//--></script>
	<table width="98%" border="0" cellspacing="0" cellpadding="4" align=center class="yosumi">
	<tr><td colspan=23>
	※「データを保存」でデータを更新しないとこのランキングに反映されません。<br>
	※長者番付は、持ち金＋普通預金預け額＋スーパー定期預け額ーローン額で決まります。</td></tr>
	<tr  class=jouge align=center bgcolor=#ffff66>
		<td>順位</td><td>名　前</td><td>性別</td><td>職　業</td><td>資　産</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>Ｌ</td><td>面</td><td>Ｈ</td><td>Ｋ</td><td>家</td>
	</tr>
EOM

#個人の家情報をunitハッシュに代入
	open(OI,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
	@ori_ie_para = <OI>;
	foreach (@ori_ie_para) {
		&ori_ie_sprit($_);
		if ($ori_k_id !~ /_/){
			$unit{"$ori_k_id"} = "<img src=\"$ori_ie_image\">";
		}
	}
	close(OI);

$i=1;

	foreach (@alldata) {
		&list_sprit($_);
		if ($list_sex eq "f") {$seibetu = "女";}else{$seibetu = "男";}
		$list_job_level = int($list_job_keiken / 100) ;
		if(!$list_kpoint){
			$list_kpoint = "0";
		}
		print <<"EOM";
<tr class=sita onmouseover="Change(this)" onmouseout="Back(this)"><td align=center>$i</td><td nowrap>$list_name</td><td align=center>$seibetu</td><td nowrap>$list_job<br>（Lv.$list_job_level）</td><td align=right nowrap>$list_sousisan円</td><td align=right>$list_kokugo</td><td align=right nowrap>$list_suugaku</td><td align=right nowrap>$list_rika</td><td align=right nowrap>$list_syakai</td><td align=right nowrap>$list_eigo</td><td align=right nowrap>$list_ongaku</td><td align=right nowrap>$list_bijutu</td><td align=right nowrap>$list_looks</td><td align=right nowrap>$list_tairyoku</td><td align=right nowrap>$list_kenkou</td><td align=right nowrap>$list_speed</td><td align=right nowrap>$list_power</td><td align=right nowrap>$list_wanryoku</td><td align=right nowrap>$list_kyakuryoku</td><td align=right nowrap>$list_love</td><td align=right nowrap>$list_unique</td><td align=right nowrap>$list_etti</td><td align=right nowrap>$list_kpointＰ</td><td align=center valign=center>$unit{"$list_k_id"}</td></tr>
EOM

		if($i >=$rankMax){last;}
			$i++;
	}
	print "</table>";
	}		#ver.1.3
	&hooter("login_view","戻る");
	exit;
}