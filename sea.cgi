#!/usr/bin/perl

$this_script = 'sea.cgi';
require './town_ini.cgi';
require './town_lib.pl';
require './event.pl';
&decode;

######################
#釣り間隔（秒）
$turi_kankaku=100;
######################

#メンテチェック
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
$seigenyou_now_time = time;
#制限時間チェック
		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}
		
#条件分岐
	if($in{'mode'} eq "sea"){&sea;}
	elsif($in{'mode'} eq "turu"){&turu;}
	elsif($in{'mode'} eq "seri"){&seri;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;
#####################################################################
sub sea{
	($next_tra0,$next_tra1,$next_tra2) = split(/=/, $next_tra);
	$nokori_time = $next_tra0 - time;
    if($nokori_time > 0){
    	$comment .= << "EOM";
		<script language="JavaScript"><!--
		var TimeID;
		var counts=$nokori_time;
		window.setTimeout("run()",1000);
		function run(){
		counts--;
		document.getElementById("time").innerHTML = counts;
		if(counts>0){timeID = setTimeout("run()",1000);}
		}
		//--></script>
    	$nameさんが釣れまであと<span id="time">$nokori_time</span>秒です。

EOM
    	}
    else{$comment .= "よ～し。釣ってやるぞ～。";}

	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;
	close(OUT);
	foreach (@myitem_hairetu){
		&syouhin_sprit($_);
		if ($syo_taikyuu <= 0){next;}
		if ($syo_syubetu eq "餌"){
			$gift_select .= "<option value=\"$syo_hinmoku\">$syo_hinmoku</option>\n";
		}
		if ($syo_syubetu eq "魚"){
			$gift_select .= "<option value=\"$syo_hinmoku\">$syo_hinmoku</option>\n";
			$seri_select .= "<option value=\"$syo_hinmoku\">$syo_hinmoku</option>\n";
		}
		if ($syo_syubetu eq "幻の魚"){
			$seri_select .= "<option value=\"$syo_hinmoku\">$syo_hinmoku</option>\n";
		}
	}

	if(!$gift_select){
		$gift_select .= "<option value=\"\">餌がありまへん。売店で買いなはれ。</option>\n";
		$comment .= "餌がなくて釣れないっぽい";
	}
	if(!$seri_select){
		$seri_select .= "<option value=\"\">出品できる物がないよ。さっさと帰りな。</option>\n";
		$comment2 .= "出品できるものはないっぽい";
	}

	&header(gym_style);
print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>●近くにいたおっちゃん<br>
	「ここはよく魚が取れるといわれている海だ。<br>餌は売店で売っているのでそれを買ってこい。<br>釣った魚を餌にしたり、売ることもできるぞ。」<br></td>
	<td  bgcolor=#333333 align=center width=35%>
	<font color="#ffffff" size="5"><b>釣りスポット</b></font>
	</td>
	</tr></table>
	
	<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi><tr>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="turu">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$k_id">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<td>
	<select name=gift_souhu>
	$gift_select
	</select>
	<input type="submit" value="釣る"></td>
	</form><td width=100% valign=top>

	<table  border="0" cellspacing="0" cellpadding="10" width=100% height=100% bgcolor=#66cc33 style="border: #663300; border-style: solid; border-width: 2px;"><tr><td><br>$comment<br></td></tr></table>

	</td></tr></table>
	<br><hr><br>
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>●近くにいたおっちゃん<br>
	「ここでは釣った魚を誰でも競りに出せる競り市場だ。<br>素人でも簡単に出せるから便利だよ。<br>魚を釣ったんだったら出してみな。」<br></td>
	<td  bgcolor=#333333 align=center width=35%>
	<font color="#ffffff" size="5"><b>競り市場</b></font>
	</td>
	</tr></table>
	
	<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi><tr>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="seri">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<td>
	<select name=seri_item>
	$seri_select
	</select>
	<input type="submit" value="出品する"></td>
	</form><td width=100% valign=top>
	
	<table  border="0" cellspacing="0" cellpadding="10" width=100% height=100% bgcolor=#66cc33 style="border: #663300; border-style: solid; border-width: 2px;"><tr><td><br>$comment2<br></td></tr></table>
	
	</td></tr></table>
	
EOM
	&hooter("login_view","戻る");
exit;
}

sub turu{
	($next_tra0,$next_tra1,$next_tra2) = split(/=/, $next_tra);
	$nokori_time = $next_tra0 - time;
    if($nokori_time > 0){&error("$nokori_time秒後まで釣れません");}

	&motimono_kensa_ev2("$in{'gift_souhu'}");
	if($kensa_flag != 1){&error("そんなもんで釣れまへん");}

	#ハッシュにしろよ馬鹿
	if($in{'gift_souhu'} eq "小魚"){$rand2="3";}
	elsif($in{'gift_souhu'} eq "ミニたこ"){$rand2="5";}
	elsif($in{'gift_souhu'} eq "ホタルイカ"){$rand2="7";}
	elsif($in{'gift_souhu'} eq "中くらいの魚"){$rand3="3";}
	elsif($in{'gift_souhu'} eq "スルメイカ"){$rand3="5";}
	elsif($in{'gift_souhu'} eq "クラゲ"){$rand3="7";}
	elsif($in{'gift_souhu'} eq "でかい魚"){$rand4="2";}
	elsif($in{'gift_souhu'} eq "ウツボ"){$rand4="3";}
	elsif($in{'gift_souhu'} eq "ミズダコ"){$rand4="5";}
	elsif($in{'gift_souhu'} eq "小エビ"){$rand1="7";}
	elsif($in{'gift_souhu'} eq "魚ルアー（小）"){$rand1="5";}
	elsif($in{'gift_souhu'} eq "魚ルアー（中）"){$rand2="5";}
	elsif($in{'gift_souhu'} eq "魚ルアー（大）"){$rand3="5";}
	else{&error("その商品は釣りには使えません。");}

	$my_rand = int(rand(3));

	if($rand1 && int(rand($rand1))+1 == 1){
		@plazentitm =(
'魚<>小魚<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>100<>0<>0<>0<>1<>回<>0<>5<>0<><>0<>0<>新鮮ピチピチです。<><><><>\n'
,'魚<>ミニたこ<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>100<>0<>0<>0<>1<>回<>0<>5<>0<><>0<>0<>ちいさいです。。<><><><>\n'
,'魚<>ホタルイカ<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>100<>0<>0<>0<>1<>回<>0<>5<>0<><>0<>0<>夜行性です。。<><><><>\n'
,'ファーストフード<>ポン・デ・リング<>0<>0<>0<>0<>0<>0<>0<>無<>0<>1<>3<>1<>0<>0<>0<>200<>1<>1<>1<>1<>回<>0<>20<>400<><><><>引っかかったのだろうか？<>0<>0<>0<>\n'
		);
	}elsif($rand2 && int(rand($rand2))+1 == 1){
		@plazentitm =(
'魚<>中くらいの魚<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>500<>0<>0<>0<>1<>回<>0<>5<>0<><>0<>0<>いわしかな？<><><><>\n'
,'魚<>クラゲ<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>500<>0<>0<>0<>1<>回<>0<>5<>0<><>0<>0<>魚？？？<><><><>\n'
,'魚<>スルメイカ<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>500<>0<>0<>0<>1<>回<>0<>5<>0<><>0<>0<>スルメにするとおいしい。<><><><>\n'
,'関西名産店<>たこ焼き<>0<>0<>0<>0<>0<>0<>0<>無<>2<>2<>2<>2<>2<>2<>2<>1000<>0<>5<>0<>1<>回<>0<>20<>500<><><><>海の中で焼かれたっぽいｗ<>0<>0<>0<>\n'
		);
	}elsif($rand3 && int(rand($rand3))+1 == 1){
		@plazentitm =(
'魚<>でかい魚<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>1000<>0<>0<>0<>1<>回<>0<>5<>0<><>0<>0<>スズキらしい<><><><>\n'
,'魚<>ウツボ<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>5000<>0<>0<>0<>1<>回<>0<>5<>0<><>0<>0<>どうやって食べるんだ？<><><><>\n'
,'魚<>ミズダコ<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>3000<>0<>0<>0<>1<>回<>0<>5<>0<><>0<>0<>どうやって食べるんだ？<><><><>\n'
,'乗り物<>ローラースルーゴーゴー<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>10000<>0<>0<>0<>4<>回<>60<>30<>0<><><><>※移動手段です。誰かが落としたんだろう。<>0<>0<>0<>\n'
		);
	}elsif($rand4 && int(rand($rand4))+1 == 1){
		@plazentitm =(
'幻の魚<>サメ<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>50000<>0<>0<>0<>1<>回<>0<>5<>0<><>0<>0<>顔が怖い！！<><><><>\n'
,'幻の魚<>海がめ<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>100000<>0<>0<>0<>1<>回<>0<>5<>0<><>0<>0<>魚じゃあないだろ！<><><><>\n'
,'幻の魚<>マグロ<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>200000<>0<>0<>0<>1<>回<>0<>5<>0<><>0<>0<>うまそ～<><><><>\n'
,'ギフト<>船艦大和の一部<>25<>25<>25<>25<>25<>25<>25<>無<>25<>25<>25<>25<>25<>25<>25<>15000000<>25<>25<>25<>1<>日<>200<>5<>0<><>150<>80<>移動手段です。<>サイリヒアデル・モブ<><><>\n'
		);
	}else{$comment="何も釣れませんでした。<br>";}
	
	$monokiroku_file="./member/$k_id/mono.cgi";
	if (! -e $monokiroku_file){open (OUT,">$monokiroku_file") || &error("自分の購入物ファイルを作成できません");}
	close(OUT);
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	@my_kounyuu_list =<OUT>;
	close(OUT);

	($syo_syubetu0,$syo_hinmoku0,$syo_kokugo0,$syo_suugaku0,$syo_rika0,$syo_syakai0,$syo_eigo0,$syo_ongaku0,$syo_bijutu0,$syo_kouka0,$syo_looks0,$syo_tairyoku0,$syo_kenkou0,$syo_speed0,$syo_power0,$syo_wanryoku0,$syo_kyakuryoku0,$syo_nedan0,$syo_love0,$syo_unique0,$syo_etti0,$syo_taikyuu0,$syo_taikyuu_tani0,$syo_kankaku0,$syo_zaiko0,$syo_cal0,$syo_siyou_date0,$syo_sintai_syouhi0,$syo_zunou_syouhi0,$syo_comment0,$syo_kounyuubi0,$tanka0,$tokubai)= split(/<>/,$plazentitm[$my_rand]);
	$kensa_flag=0;
	@new_myitem_hairetu = ();

	foreach $one_kounyuu_item (@my_kounyuu_list){
		&syouhin_sprit ($one_kounyuu_item);
		if ($syo_syubetu0 && $syo_hinmoku0 && $syo_syubetu eq $syo_syubetu0 && $syo_hinmoku eq $syo_hinmoku0){
			$syo_taikyuu += $syo_taikyuu0;
			$motikosuu = int($syo_taikyuu / $syo_taikyuu0);
			if ($syo_taikyuu % $syo_taikyuu0 > 0){$motikosuu++;}
			if ($item_kosuuseigen < $motikosuu){&error("せっかく釣ったけどもう持ちきれません。");}
			$kensa_flag = 1;
		}
		&syouhin_temp;
		push @new_myitem_hairetu,$syo_temp;
	}

	if ($kensa_flag != 1){
		if (@my_kounyuu_list >= $syoyuu_gendosuu){&error("せっかく釣ったけどもう持ちきれません。");}
		$syo_kounyuubi0 = time;
		$syo_temp0="$syo_syubetu0<>$syo_hinmoku0<>$syo_kokugo0<>$syo_suugaku0<>$syo_rika0<>$syo_syakai0<>$syo_eigo0<>$syo_ongaku0<>$syo_bijutu0<>$syo_kouka0<>$syo_looks0<>$syo_tairyoku0<>$syo_kenkou0<>$syo_speed0<>$syo_power0<>$syo_wanryoku0<>$syo_kyakuryoku0<>$syo_nedan0<>$syo_love0<>$syo_unique0<>$syo_etti0<>$syo_taikyuu0<>$syo_taikyuu_tani0<>$syo_kankaku0<>$syo_zaiko0<>$syo_cal0<>$syo_siyou_date0<>$syo_sintai_syouhi0<>$syo_zunou_syouhi0<>$syo_comment0<>$syo_kounyuubi0<>$tanka0<>$tokubai0<>\n";
		push @new_myitem_hairetu,$syo_temp0;
	}
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_hairetu;
	close(OUT);

	$now_time=time;
	$next_tra0 = $now_time + $turi_kankaku;
	$next_tra = "$next_tra0=$next_tra1=$next_tra2=";

	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
	
	if(!$syo_hinmoku0){$comment="何も釣れませんでした。<br>";}
	else{$comment="$syo_hinmoku0がつりあがりました！<br>";}

	&sea;
}

sub seri{
	#ハッシュにしろよ馬鹿
	if($in{'seri_item'} eq "小魚"){$kati1="100";}
	if($in{'seri_item'} eq "ミニたこ"){$kati1="100";}
	if($in{'seri_item'} eq "ホタルイカ"){$kati1="100";}
	if($in{'seri_item'} eq "中くらいの魚"){$kati2="500";}
	if($in{'seri_item'} eq "スルメイカ"){$kati2="500";}
	if($in{'seri_item'} eq "クラゲ"){$kati2="500";}
	if($in{'seri_item'} eq "でかい魚"){$kati3="1000";}
	if($in{'seri_item'} eq "ウツボ"){$kati3="5000";}
	if($in{'seri_item'} eq "ミズダコ"){$kati3="3000";}
	if($in{'seri_item'} eq "サメ"){$kati4="50000";}
	if($in{'seri_item'} eq "海がめ"){$kati4="100000";}
	if($in{'seri_item'} eq "マグロ"){$kati4="200000";}

	&motimono_kensa_ev2("$in{'seri_item'}");
	if($kensa_flag != 1){&error("そんなもん出品できまへん");}

	if($kati1 ne ""){
		$kati=int(rand($kati1))+1;
		$kati+=50;
		$comment2="$in{'seri_item'}が$kati円で売れました！";
	}elsif($kati2 ne ""){
		$kati=int(rand($kati2))+1;
		$kati+=200;
		$comment2="$in{'seri_item'}が$kati円で売れました！";
	}elsif($kati3 ne ""){
		$kati=int(rand($kati3))+1;
		$kati+=2500;
		$comment2="$in{'seri_item'}が$kati円で売れました！";
	}elsif($kati4 ne ""){
		$kati=int(rand($kati4))+1;
		$kati +=50000;
		$comment2="$in{'seri_item'}が$kati円で売れました！";
	}else{
		$comment2="そんな商品に価値なんかねえな。";
	}

	$money+= $kati;
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);

	&sea;
}