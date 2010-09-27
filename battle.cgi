#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
#################################
#Edit:　ロー
#################################
$bbfile = "./dat_dir/battle.cgi";

$this_script = 'battle.cgi';
require './town_ini.cgi';
require './town_lib.pl';
&decode;
#メンテチェック

	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
$seigenyou_now_time = time;
#制限時間チェック
		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}

#条件分岐
	if($in{'mode'} eq "bbin"){&bbin;}
	elsif($in{'mode'} eq "bb"){&bb;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;


#############以下サブルーチン
sub bbin {
	&header(gym_style);

	print <<"EOM";
	<table width="500px" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>モンスターバトル。凶\暴\な魔物を相手に戦います。</td>
	<td  bgcolor=#333333 align=center><Font Size="5" Color="white">ＭＢ</Font></td>
	</tr></table>

<table style="FONT-SIZE: x-small; BACKGROUND-COLOR: #ffffff" cellspacing="3" cellpadding="3" width="500px" border="1" align="center">
<tr><td><br>
Ｓランク：神でも恐れるモンスターが沢山います。<br>
Ａランク：プロ級のハンターでも、苦戦するモンスターがいます。<br>
Ｂランク：中級ハンター向け。推奨値（頭脳エネ+身体エネ）：8000<br>
Ｃランク：初級ハンター向け。推奨値（頭脳エネ+身体エネ）：2000<br>
Ｄランク：ヒヨコハンター向け。推奨値（頭脳エネ+身体エネ）：500<br>
<br>
</td></tr>
<tr><td>
<form method="POST" action="$this_script">
<input type=hidden name=command value="srank">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>bb<>">
<input type=submit name=srank value=Ｓランク闘技場>
</form>
</td></tr>
<tr><td>　
<form method="POST" action="$this_script">
<input type=hidden name=command value="arank">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>bb<>">
<input type=submit name=srank value=Ａランク闘技場>
</form>
</td></tr>
<tr><td>
<form method="POST" action="$this_script">
<input type=hidden name=command value="brank">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>bb<>">
<input type=submit name=srank value=Ｂランク闘技場>
</form>
</td></tr>
<tr><td>　
<form method="POST" action="$this_script">
<input type=hidden name=command value="crank">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>bb<>">
<input type=submit name=srank value=Ｃランク闘技場>
</form>
</td></tr>
<tr><td>　
<form method="POST" action="$this_script">
<input type=hidden name=command value="drank">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>bb<>">
<input type=submit name=srank value=Ｄランク闘技場>
</form>
</td></tr>
</table>
<br><br>
EOM

 	&hooter("login_view","戻る");

}


sub bb {
	open(IN,"< $bbfile") || &error("Open Error : $bbfile");
	eval{ flock (IN, 1); };
	@bb_erabi = <IN>;
	close(IN);

	foreach (@bb_erabi){
		($bb_rank,$bb_id,$bb_name,$bb_gazou,$bb_money,$bb_itembangou,$bb_itembangou2,$bb_itemname,$bb_itemname2,$bb_nou_energy,$bb_energy,$bb_yobi3) = split(/<>/);
	if($bb_rank eq 's'){
	push @s_rank,$_;
	next;
	}
	if($bb_rank eq 'a'){
	push @a_rank,$_;
	next;
	}
	if($bb_rank eq 'b'){
	push @b_rank,$_;
	next;
	}
	if($bb_rank eq 'c'){
	push @c_rank,$_;
	next;
	}
	if($bb_rank eq 'd'){
	push @d_rank,$_;
	next;
	}


	}

	if ($in{'command'} eq "srank"){
	@bb_erabi = (@s_rank);
	}elsif($in{'command'} eq "arank"){
	@bb_erabi = (@a_rank);
	}elsif($in{'command'} eq "brank"){
	@bb_erabi = (@b_rank);
	}elsif($in{'command'} eq "crank"){
	@bb_erabi = (@c_rank);
	}else{
	@bb_erabi = (@d_rank);
	}

	$randed= int (rand($#bb_erabi+1));
 	$bb_erabi=splice(@bb_erabi,$randed,1);
	@bb_nouryoku_suuzi_hairetu = split(/<>/,$bb_erabi);
	($bb_rank,$bb_id,$bb_name,$bb_gazou,$bb_money,$bb_itembangou,$bb_itembangou2,$bb_itemname,$bb_itemname2,$bb_nou_energy,$bb_energy,$bb_yobi3) = split(/<>/, $bb_erabi);

	#アイコンがあれば代入
	&header;

	print <<"EOM";
	<br><br><table width="600" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr align=center><td>
<table border="0"  cellspacing="0" cellpadding="1" style=" border: $st_win_wak; border-style: solid; border-width: 1px;"  width=150>
<tr><td align=center colspan=2 bgcolor=#ccff66 >
$icon_hyouzi_a$nameさん
</td></tr>
<tr><td align=right><span class=honbun3>頭脳パワー</span>：</td><td>$nou_energy</td></tr>
<tr><td align=right><span class=honbun3>身体パワー</span>：</td><td>$energy</td></tr>
</table>
	</td><td><IMG SRC="./monster/$bb_gazou"><br><br>
	<div class=tyuu>$bb_nameが現れた！</div><br><br>
	<div class=dai>Fight start !!</div>
	</td><td>
<table border="0"  cellspacing="0" cellpadding="1" style=" border: $st_win_wak; border-style: solid; border-width: 1px;"  width=150>
<tr><td align=center colspan=2 bgcolor=#ffcc99>
$bb_name
</td></tr>
<tr><td align=right><span class=honbun3>頭脳パワー</span>：</td><td>$bb_nou_energy</td></tr>
<tr><td align=right><span class=honbun3>身体パワー</span>：</td><td>$bb_energy</td></tr>
</table>
	</td></tr></table>
EOM

    if(!$buki){
        $buki="0/50/∞/1/0/";
        $buki_name="素手";
    }
    if(!$bougu){
        $bougu="0/50/∞/1/0/";
        $bougu_name="洋服";
    }
    if(!$mahou){
        $mahou="0/50/∞/1/0/";
        $mahou_name="念力";
    }
    if(!$omamori){
        $omamori="0/50/∞/1/0/";
        $omamori_name="先祖の霊";
    }
    ($buki_iryoku,$buki_meityu,$buki_kaisuu,$buki_lv,$buki_keiken)=split(/\//,$buki);
    ($bougu_iryoku,$bougu_meityu,$bougu_kaisuu,$bougu_lv,$bougu_keiken)=split(/\//,$bougu);
    ($mahou_iryoku,$mahou_meityu,$mahou_kaisuu,$mahou_lv,$mahou_keiken)=split(/\//,$mahou);
    ($omamori_iryoku,$omamori_meityu,$omamori_kaisuu,$omamori_lv,$omamori_keiken)=split(/\//,$omamori);
    
	if ($speed > $bb_energy){$turn =1;}
	$sentou_kaisuu =0;
	foreach (1..50){
			print "<br><br><table width=\"600\" border=\"0\" cellspacing=\"0\" cellpadding=\"5\" align=center class=yosumi><tr><td colspan=2>";
			if ($turn == 1){&kougekibb (1,$name);			#自分の攻撃
			}else{&kougekibb (0,$bb_name);}			#相手の攻撃
			print <<"EOM";
			</td></tr>
			<tr><td align=left>
			<div class=tyuu>頭脳パワー：$nou_energy</div>
			<div class=tyuu>身体パワー：$energy</div><br>
			<div class=tyuu>種類：名前/威力/命中（回避）率/使用可\能\回\数/レベル/経験地/</div>
			<div class=tyuu>武器：$buki_name/$buki</div>
			<div class=tyuu>防具：$bougu_name/$bougu</div>
			<div class=tyuu>魔法：$mahou_name/$mahou</div>
			<div class=tyuu>御守：$omamori_name/$omamori</div>
			</td>
			<td align=right>
			<div class=tyuu>頭脳パワー：$bb_nou_energy</div>
			<div class=tyuu>身体パワー：$bb_energy</div>
			</td></tr></table>
EOM
			$sentou_kaisuu ++;
			if ($bb_energy <= 0){$win_flag=1;last;}
			if ($bb_nou_energy <= 0){$win_flag=2;last;}
			if ($energy <= 0){$win_flag=3;last;}
			if ($nou_energy <= 0){$win_flag=4;last;}
			if ($turn == 1){$turn = 0;} else {$turn = 1;}
	}
	print "<br><br>";

	if ($energy < 0){$energy = 0;}
	if ($nou_energy < 0){$nou_energy = 0;}
	
	$hassei_rand1 = int(rand(10))+1;
		if ($hassei_rand1 == 1){
			$getitem = $bb_itembangou2;
			$getitemn = $bb_itemname2;
		}else{
			$getitem = $bb_itembangou;
			$getitemn = $bb_itemname;
		}

$hassei_rand = int(rand(5))+1;
if ($hassei_rand == 1){
	if ($win_flag == 1) {
		print "<div align=center style=\"color:#339933;font-size:14px;\">勝ちました！<br>逃げている$bb_nameが<br>$bb_money円を落として行った。$getitemnをGETしました。<br>Ｋポイントが３Ｐあがりました。</div>";
		$money += $bb_money;
		$kpoint+=3;
		&otosi_item($getitem);
	}elsif($win_flag == 2){
		print "<div align=center style=\"color:#339933;font-size:14px;\">勝ちました！<br>脅えている$bb_nameが<br>$bb_money円をさしだしました。$getitemnをGETしました。<br>Ｋポイントが３Ｐあがりました。</div>";
		$money += $bb_money;
		$kpoint+=3;
		&otosi_item($getitem);
	}elsif($win_flag == 3){
		print "<div align=center style=\"color:#ff3300;font-size:14px;\">負けてしまいました。。<br>ボロボロになった$nameさんの財布から<br>所持金の半分を奪われました。</div>";
		$money = int ($money / 2);
	}elsif($win_flag == 4){
		print "<div align=center style=\"color:#ff3300;font-size:14px;\">負けてしまいました。。<br>意識がもうろうとした$nameさんの財布から<br>所持金の半分を奪われました。</div>";
		$money = int ($money / 2);
	}else{
		print "決着がつきませんでした。。<br>しかし、相手は金を落として行った。<br>$bb_money円を手に入れた。";
		$money += $bb_money;
	}

}else{

	if ($win_flag == 1) {
		print "<div align=center style=\"color:#339933;font-size:14px;\">勝ちました！<br>逃げている$bb_nameが<br>$bb_money円を落として行った。<br>Ｋポイントが１Ｐあがりました。</div>";
		$money += $bb_money;
		$kpoint++;
	}elsif($win_flag == 2){
		print "<div align=center style=\"color:#339933;font-size:14px;\">勝ちました！<br>脅えている$bb_nameが<br>$bb_money円をさしだしました。<br>Ｋポイントが１Ｐあがりました。</div>";
		$money += $bb_money;
		$kpoint++;
	}elsif($win_flag == 3){
		print "<div align=center style=\"color:#ff3300;font-size:14px;\">負けてしまいました。。<br>ボロボロになった$nameさんの財布から<br>$bb_money円を奪われました。</div>";
		$money -= $bb_money;
	}elsif($win_flag == 4){
		print "<div align=center style=\"color:#ff3300;font-size:14px;\">負けてしまいました。。<br>意識がもうろうとした$nameさんの財布から<br>$bb_money円を奪われました。</div>";
		$money -= $bb_money;
	}else{
		print "決着がつきませんでした。。";
	}
}

		&hooter("login_view","戻る");
#データ更新
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
	exit;
}

sub kougekibb {
#攻撃内容をランダムで選択


		$battle_rand = int(rand(2))+1;


		print "<table width=\"600\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" align=center><tr align=center><td>";
##自分の攻撃の場合
		if (@_[0] == 1){
			print "<div style=\"color:#339933;font-size:12px;\" align=left>@_[1]の攻撃！<br>";
#攻撃内容
			&kougekinaiyoubb (1,$bb_name);
#結果表示

			if ($damage eq "no_d"){

					print "<div style=\"color:#ff3300;font-size:12px;\" align=right>$return_naiyou</div>\n";
			}else{

					print "<div style=\"color:#339933;font-size:12px;\" align=right>$return_naiyou</div>\n";
					if ($battle_rand == 1){
						$bb_nou_energy -= $damage;
					}else{
						$bb_energy -= $damage;
					}
			}
			
##相手の攻撃の場合
		}else {
			print "<div style=\"color:#ff3300;font-size:12px;\" align=right>@_[1]の攻撃！<br>";
			&kougekinaiyoubb (0,$name);
#結果表示
#自分にきかない場合
			if ($damage eq "no_d"){
					print "<div style=\"color:#339933;font-size:12px;\" align=left>$return_naiyou</div>\n";
			}else{
#ダメージを受けた場合
					print "<div style=\"color:#ff3300;font-size:12px;\" align=left>$return_naiyou</div>\n";
#頭脳ダメージ
					if ($battle_rand == 1){
						$nou_energy -= $damage;
					}else{
#肉体ダメージ
						$energy -= $damage;
					}
			}
		}
	print "</td></tr></table>";
}

###攻撃内容ごとのダメージ処理サブルーチン
sub kougekinaiyoubb {
# @_[0]＝1なら自分の攻撃、0なら相手の攻撃
	if (@_[0] == 1){$align_settei = "align=left";}else{$align_settei = "align=right";}

		if ($battle_rand ==1){
			print "@_[1]に魔法で攻撃！</div><br>\n";
			&iryoku_hanteibb (@_[0],1);
			if ($damage eq "no_d"){$return_naiyou = "$comment<br>@_[1]にダメージを与えることができなかった。";}
			else{$return_naiyou = "$comment<br>@_[1]は<span style=\"font-size:18px\">$damage</span> の精神的ダメージを受けた！";}
		}


		if ($battle_rand ==2){
			print "@_[1]に武器で攻撃！</div><br>\n";
			&iryoku_hanteibb (@_[0],2);
			if ($damage eq "no_d"){$return_naiyou = "$comment<br>@_[1]にダメージを与えることができなかった。";}
			else{$return_naiyou = " $comment<br>@_[1]は<span style=\"font-size:18px\">$damage</span> の身体ダメージを受けた！";}
		}

}

#威力判定サブルーチン
sub iryoku_hanteibb {
#攻撃の内容ごとの能力値
    $comment="";
    $buki_owata="";
    $bougu_owata="";
    $mahou_owata="";
    $omamori_owata="";
    $mae_soubi="";
    
    $rand = int(rand(100))+1;
	if ($battle_rand ==1){
	
		if (@_[0] == 1){
		
		    $nou_iryoku=int($nou_energy/10);
		    $nou_iryoku=int(rand($nou_iryoku))+1;
		    if($rand<$mahou_meityu){
		        $hantei_kakkati=$nou_iryoku+$mahou_iryoku;
		        if($mahou_name ne "念力"){$mahou_kaisuu--;}
		        $mahou_keiken++;
		        $comment.="魔法が当たった！（ダメージ：$nou_iryoku  ＋  $mahou_iryoku  ＝  $hantei_kakkati）<br>";
		            if($mahou_keiken>=$mahou_lv*10){
		                $mahou_lv++;
		                $mahou_keiken=0;
		                $mahou_iryoku+=$mahou_lv;
		                $comment.="レベルが上がった！（魔力が  $mahou_lv  うｐ！）<br>";
		                    if(int(rand($mahou_lv))+1 == 1){
		                        $mahou_meityu+=$mahou_lv;
		                        $comment.="命中率も  $mahou_lv  あがった！<br>";
		                    }
		            }
		            if($mahou_kaisuu<=0 && $mahou_name ne "念力"){
		                $mahou_owata="yes";
		                $comment.="<b>魔法が使えなくなってしまった！</b><br>";
		            }
		    }else{
		        $comment.="魔法は当たらなかった・・・<br>";
		        $hantei_kakkati=0;
		    }
		    
		}else{
		
		    $nou_iryoku=int($bb_nou_energy/10);
		    if($rand<$omamori_meityu){
		        $comment.="魔法をさけることができた！<br>";
		        $hantei_kakkati=0;
		    }else{
		        $hantei_kakkati=$nou_iryoku-$omamori_iryoku;
		        if($omamori_name ne "先祖の霊"){$omamori_kaisuu--;}
		        $omamori_keiken++;
		        $comment.="魔法をさけることはできなかった・・・（ダメージ$nou_iryoku  －  $omamori_iryoku  ＝  $hantei_kakkati）<br>";
		            if($omamori_keiken>=$omamori_lv*10){
		                $omamori_lv++;
		                $omamori_keiken=0;
		                $omamori_iryoku+=$omamori_lv;
		                $comment.="レベルが上がった！（守力が  $omamori_lv  うｐ！）<br>";
		                    if(int(rand($omamori_lv))+1 == 1){
		                        $omamori_meityu+=$omamori_lv;
		                        $comment.="回避率も  $omamori_lv  あがった！<br>";
		                    }
		            }
		            if($omamori_kaisuu<=0 && $omamori_name ne "先祖の霊"){
		                $omamori_owata="yes";
		                $comment.="<b>御守が使えなくなってしまった！</b><br>";
		            }
		    }
		    
		}
	}else{
		if (@_[0] == 1){
		
		    $iryoku=int($energy/10);
		    $iryoku=int(rand($iryoku))+1;
		    if($rand<$buki_meityu){
		        $hantei_kakkati=$iryoku+$buki_iryoku;
		        if($buki_name ne "素手"){$buki_kaisuu--;}
		        $buki_keiken++;
		        $comment.="攻撃が当たった！（ダメージ：$iryoku  ＋  $buki_iryoku  ＝  $hantei_kakkati）<br>";
		            if($buki_keiken>=$buki_lv*10){
		                $buki_lv++;
		                $buki_keiken=0;
		                $buki_iryoku+=$buki_lv;
		                $comment.="レベルが上がった！（攻撃力が  $buki_lv  うｐ！）<br>";
		                    if(int(rand($buki_lv))+1 == 1){
		                        $buki_meityu+=$buki_lv;
		                        $comment.="命中率も  $buki_lv  あがった！<br>";
		                    }
		            }
		            if($buki_kaisuu<=0 && $buki_name ne "素手"){
		                $buki_owata="yes";
		                $comment.="<b>武器が使えなくなってしまった！</b><br>";
		            }
		    }else{
		        $comment.="攻撃は当たらなかった・・・<br>";
		        $hantei_kakkati=0;
		    }
		    
		}else{
		
		    $iryoku=int($bb_energy/10);
		    if($rand<$bougu_meityu){
		        $comment.="攻撃をさけることができた！<br>";
		        $hantei_kakkati=0;
		    }else{
		        $hantei_kakkati=$iryoku-$bougu_iryoku;
		        if($bougu_name ne "洋服"){$bougu_kaisuu--;}
		        $bougu_keiken++;
		        $comment.="攻撃をさけることはできなかった・・・（ダメージ$iryoku  －  $bougu_iryoku  ＝  $hantei_kakkati）<br>";
		            if($bougu_keiken>=$bougu_lv*10){
		                $bougu_lv++;
		                $bougu_keiken=0;
		                $bougu_iryoku+=$bougu_lv;
		                $comment.="レベルが上がった！（防御力が  $bougu_lv  うｐ！）<br>";
		                    if(int(rand($bougu_lv))+1 == 1){
		                        $bougu_meityu+=$bougu_lv;
		                        $comment.="回避率も  $bougu_lv  あがった！<br>";
		                    }
		            }
		            if($bougu_kaisuu<=0 && $bougu_name ne "洋服"){
		                $bougu_owata="yes";
		                $comment.="<b>防具が使えなくなってしまった！</b><br>";
		            }
		    }
		    
		}
	}

	if ($hantei_kakkati <= 0){
			$damage = "no_d";
	}else{
			$damage = "$hantei_kakkati";
	}
	
	open(OUT,"< ./member/$k_id/mono.cgi") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	@my_kounyuu_list =<OUT>;
	close(OUT);
#データ更新

    $buki="$buki_iryoku/$buki_meityu/$buki_kaisuu/$buki_lv/$buki_keiken/";
    $bougu="$bougu_iryoku/$bougu_meityu/$bougu_kaisuu/$bougu_lv/$bougu_keiken/";
    $mahou="$mahou_iryoku/$mahou_meityu/$mahou_kaisuu/$mahou_lv/$mahou_keiken/";
    $omamori="$omamori_iryoku/$omamori_meityu/$omamori_kaisuu/$omamori_lv/$omamori_keiken/";
    
    if($buki_owata eq "yes"){
        $mae_soubi="武器<>$buki_name<>$buki_iryoku<>$buki_meityu<>$buki_kaisuu<>$buki_lv<>$buki_keiken<>\n";
        $buki="0/50/∞/1/0/";
        $buki_name="素手";
    }
    if($bougu_owata eq "yes"){
        $mae_soubi="防具<>$bougu_name<>$bougu_iryoku<>$bougu_meityu<>$bougu_kaisuu<>$bougu_lv<>$bougu_keiken<>\n";
        $bougu="0/50/∞/1/0/";
        $bougu_name="洋服";
    }
    if($mahou_owata eq "yes"){
        $mae_soubi="魔法<>$mahou_name<>$mahou_iryoku<>$mahou_meityu<>$mahou_kaisuu<>$mahou_lv<>$mahou_keiken<>\n";
        $mahou="0/50/∞/1/0/";
        $mahou_name="念力";
    }
    if($omamori_owata eq "yes"){
        $mae_soubi="御守<>$omamori_name<>$omamori_iryoku<>$omamori_meityu<>$omamori_kaisuu<>$omamori_lv<>$omamori_keiken<>\n";
        $omamori="0/50/∞/1/0/";
        $omamori_name="先祖の霊";
    }
    
    ($buki_iryoku,$buki_meityu,$buki_kaisuu,$buki_lv,$buki_keiken)=split(/\//,$buki);
    ($bougu_iryoku,$bougu_meityu,$bougu_kaisuu,$bougu_lv,$bougu_keiken)=split(/\//,$bougu);
    ($mahou_iryoku,$mahou_meityu,$mahou_kaisuu,$mahou_lv,$mahou_keiken)=split(/\//,$mahou);
    ($omamori_iryoku,$omamori_meityu,$omamori_kaisuu,$omamori_lv,$omamori_keiken)=split(/\//,$omamori);
    
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
			
    if($mae_soubi){
        open(OUT,"< ./member/$k_id/mono.cgi") || &error("自分の購入物ファイルが開けません");
        eval{ flock (OUT, 1); };
        @my_item_list = <OUT>;
        close(OUT);
        
        unshift (@my_item_list,$mae_soubi);
	    
	    open(OUT,">./member/$k_id/mono.cgi") || &error("自分の購入物ファイルが開けません");
	    eval{ flock (OUT, 2); };
	    print OUT @my_item_list;
	    close(OUT);
    }
}

# 魔物の核
sub otosi_item {

#0薬草
#1上薬草
#2特薬草
#3秘伝薬草

	$getitm = $_[0];
#	0=英文解釈教室 1=成り上がり 2=おばあちゃんの知恵袋 今はこれだけ　持ち物オーバーでも増えていきます。規制は入っていません。
	@plazentitm =(
'MB<>薬草<>0<>0<>0<>0<>0<>0<>0<>万能,5<>0<>3<>3<>0<>0<>0<>0<>100<>0<>0<>0<>1<><>5<>5<>0<><>0<>0<><>ロー<><><>\n'
,'MB<>上薬草<>0<>0<>0<>0<>0<>0<>0<>万能,10<>0<>5<>5<>0<>0<>0<>0<>500<>0<>0<>0<>1<><>10<>5<>0<><>0<>0<><>ロー<><><>\n'
,'MB<>特薬草<>0<>0<>0<>0<>0<>0<>0<>万能,15<>0<>10<>10<>0<>0<>0<>0<>5000<>0<>0<>0<>1<><>15<>5<>0<><>0<>0<><>ロー<><><>\n'
,'MB<>秘伝薬草<>0<>0<>0<>0<>0<>0<>0<>万能,20<>0<>50<>50<>0<>0<>0<>0<>50000<>0<>0<>0<>1<><>20<>5<>0<><>0<>0<><>ロー<><><>\n'
,'MB<>ドラゴンの角<>30000<>30000<>30000<>30000<>30000<>30000<>30000<>無<>30000<>30000<>30000<>30000<>30000<>30000<>30000<>1000000000<>30000<>30000<>30000<>1<><>30<>5<>0<><>9000<>9000<>伝説のアイテム。常に光輝いている。<>ロー<><><>\n'
);
	if ($#plazentitm < $getitm){&error("その品物は準備されていません。");}

	if(!$k_id){&error("mono.cgi エラー event5")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";
	if (! -e $monokiroku_file){open (OUT,">$monokiroku_file") || &error("自分の購入物ファイルを作成できません");}
	close(OUT);
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	@my_kounyuu_list =<OUT>;
	close(OUT);

	if (@my_kounyuu_list >= $syoyuu_gendosuu){$kensa_flag=2;return;} # 持ち物オーバーで検査フラグを立てて帰る。


	($syo_syubetu0,$syo_hinmoku0,$syo_kokugo0,$syo_suugaku0,$syo_rika0,$syo_syakai0,$syo_eigo0,$syo_ongaku0,$syo_bijutu0,$syo_kouka0,$syo_looks0,$syo_tairyoku0,$syo_kenkou0,$syo_speed0,$syo_power0,$syo_wanryoku0,$syo_kyakuryoku0,$syo_nedan0,$syo_love0,$syo_unique0,$syo_etti0,$syo_taikyuu0,$syo_taikyuu_tani0,$syo_kankaku0,$syo_zaiko0,$syo_cal0,$syo_siyou_date0,$syo_sintai_syouhi0,$syo_zunou_syouhi0,$syo_comment0,$syo_kounyuubi0,$tanka0,$tokubai)= split(/<>/,$plazentitm[$getitm]);

	$kensa_flag=0;
	@new_myitem_hairetu = ();
	foreach $one_kounyuu_item (@my_kounyuu_list){
		&syouhin_sprit ($one_kounyuu_item);
		if ($syo_syubetu eq $syo_syubetu0 && $syo_hinmoku eq $syo_hinmoku0){
			$syo_taikyuu += $syo_taikyuu0;
			$kensa_flag = 1;
		}
		&syouhin_temp;
		push @new_myitem_hairetu,$syo_temp;
	}
	if ($kensa_flag != 1){
		$syo_kounyuubi0 = time;
		$syo_temp0="$syo_syubetu0<>$syo_hinmoku0<>$syo_kokugo0<>$syo_suugaku0<>$syo_rika0<>$syo_syakai0<>$syo_eigo0<>$syo_ongaku0<>$syo_bijutu0<>$syo_kouka0<>$syo_looks0<>$syo_tairyoku0<>$syo_kenkou0<>$syo_speed0<>$syo_power0<>$syo_wanryoku0<>$syo_kyakuryoku0<>$syo_nedan0<>$syo_love0<>$syo_unique0<>$syo_etti0<>$syo_taikyuu0<>$syo_taikyuu_tani0<>$syo_kankaku0<>$syo_zaiko0<>$syo_cal0<>$syo_siyou_date0<>$syo_sintai_syouhi0<>$syo_zunou_syouhi0<>$syo_comment0<>$syo_kounyuubi0<>$tanka0<>$tokubai0<>\n";
		push @new_myitem_hairetu,$syo_temp0;
	}
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_hairetu;
	close(OUT);	
}

