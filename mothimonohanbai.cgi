#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。

# 扱える上限数値
$mothi_jougen = 25;
#--------------------------

$this_script = 'mothimonohanbai.cgi';
require './town_ini.cgi';
require './town_lib.pl';
require './motimono_hanbai.pl';
&decode;

#条件分岐

	if($in{'mode'} eq "motimono_hanbai"){&motimono_hanbai;} #'./motimono_hanbai.pl'になります。
	if($in{'mode'} eq "mothi_do"){&mothi_do;}
	if($in{'mode'} eq "mothi_baikyaku"){&mothi_baikyaku;}
	if($in{'mode'} eq "mothi_baikyaku_do"){&mothi_baikyaku_do;}

	else{&error("「戻る」ボタンで街に戻ってください");}
exit;

##### 購入処理 #################
sub mothi_do{
	($in{'ori_ie_id'},$bangou2) = split(/_/, $in{'ori_ie_id'});
	$hausu_no = $in{'ori_ie_id'};
#	$in{'ori_ie_id'} = "$in{'ori_ie_id'}".'_'."3";

	$aitesaki_fail= "./member/$hausu_no/3_log.cgi";#$hausu_no
	open(IN,"< $aitesaki_fail") || &error("Open Error : $aitesaki_fail");
	eval{ flock (IN, 1); };
	$my_para = <IN>;
	@koniyusiyouhin = <IN>;
	close(IN);

	if ($in{'koniyubangou'} eq ""){&error("購入番号がありません。");}
	$koniyusiyouhin = $koniyusiyouhin[$in{'koniyubangou'}];

	($syo_syubetu,$syo_hinmoku,$syo_kokugo,$syo_suugaku,$syo_rika,$syo_syakai,$syo_eigo,$syo_ongaku,$syo_bijutu,$syo_kouka,$syo_looks,$syo_tairyoku,$syo_kenkou,$syo_speed,$syo_power,$syo_wanryoku,$syo_kyakuryoku,$syo_nedan,$syo_love,$syo_unique,$syo_etti,$syo_taikyuu,$syo_taikyuu_tani,$syo_kankaku,$syo_zaiko,$syo_cal,$syo_siyou_date,$syo_sintai_syouhi,$syo_zunou_syouhi,$syo_comment,$syo_kounyuubi,$tanka,$tokubai)= split(/<>/,$koniyusiyouhin);
#koko2006/12/11
	if ($in{'syouhin'} ne $syo_hinmoku){&error("$in{'syouhin'} 購入番号と商品名が違ってます。もう一度確かめて。",'botan');} #errorを改造してあります。
#kokoend
#	if (!($syo_syubetu eq "食料品" || $syo_syubetu eq "ファーストフード")){
#		$syo_syubetu = "リサイクル";
#	}

	if(!$k_id){&error("mono.cgi エラー mothimonohanbai1")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;
	close(OUT);
#koko2007/11/21
	foreach $data (@myitem_hairetu){
		$aitm_hiretu = (split(/<>/,$data))[0];

		$kuka_basyo = (split(/<>/,$data))[9];
		if ($kuka_basyo =~ /食料品/ and $aitm_hiretu eq "ギフト商品"){
			$aitm_hiretu = "食料品";
			&syouhin_sprit($myitem_hairetu[$i]);
			$syo_syubetu = "食料品";
			&syouhin_temp;
			$myitem_hairetu[$i] = $syo_temp;
		}
		if ($kuka_basyo =~ /ファ/ and $aitm_hiretu  eq "ギフト商品"){
			$aitm_hiretu = "ファーストフード";
			&syouhin_sprit($myitem_hairetu[$i]);
			$syo_syubetu = "ファーストフード";
			&syouhin_temp;
			$myitem_hairetu[$i] = $syo_temp;
		}
		$i++;

		if ($aitm_hiretu eq "ギフト商品"){
			push @aitem_giftsyo,$data;
		}elsif ($aitm_hiretu eq "ギフト"){ #koko2006/12/31
			push @aitem_gift,$data; #koko2006/12/31
		}else{
			push @aitem_sonota,$data;
		}
	}
#end2007/11/21
	if ($k_id ne $hausu_no){
		if($#aitem_sonota + 1 > $syoyuu_gendosuu){&error("持ち物が所有限度を超します。");}
		if ($in{'siharaihouhou'} eq "現金"){
			if ($syo_nedan > $money){&error("お金が足りません");}
			$money -= $syo_nedan;
		}elsif ($in{'siharaihouhou'} ne "現金"){
			if($bank - $syo_nedan < 0){&error("$in{'siharaihouhou'} 貯金がありません。");} #2007/03/19
			$bank -= $syo_nedan;
			&kityou_syori("支払い（$syo_hinmoku）","$syo_nedan","",$bank,"普");
		}
	}

#相手の銀行に振り込み＆記帳処理
		if ($k_id ne $hausu_no){		#自分の店なら売上金は入らない
			&openAitelog ($in{'ori_ie_id'});
			$aite_bank += $syo_nedan;
			&aite_kityou_syori("販売2（$syo_hinmoku） => $in{'name'}さん","",$syo_nedan,$aite_bank,"普",$hausu_no,"lock_off");#koko 2005/03/16
	
			&aite_temp_routin;
			open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
			eval{ flock (OUT, 2); };
			print OUT $aite_k_temp;
			close(OUT);
		}else{
			$money -= 500;
		}





	$syo_kounyuubi = time;
	if ($k_id ne $hausu_no){$baikyaku_hyouzi = $syo_nedan;}
	if(!$baikyaku_hyouzi){$baikyaku_hyouzi ="-500";}
	$money -= $baikyaku_hyouzi;
###売り場の商品を減らす
	splice @koniyusiyouhin,$in{'koniyubangou'},1;

	open(OUT,">$aitesaki_fail") || &error("Write Error : $aitesaki_fail");
	eval{ flock (OUT, 2); };
	print OUT $my_para;
	print OUT @koniyusiyouhin;
	close(OUT);	

##自分の持ち物を増やす

	&syouhin_temp;			#ver.1.3
	push (@myitem_hairetu,$syo_temp);			#ver.1.3

	#自分の所有物ファイルを更新
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @myitem_hairetu;
	close(OUT);
#ログ更新
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);

	&header;
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
●$syo_hinmoku [$in{'koniyubangou'}]($baikyaku_hyouzi円)を仕入れました。
</span>
</td></tr></table>
<br>
	<form method=POST action="$this_script">
	<input type=hidden name=mode value="motimono_hanbai">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
	<input type=submit value="購入を続ける">
	</form>
	<form method=POST action="$script">
	<input type=hidden name=mode value="login_view">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="戻る">
	</form>
	</div>
	</body></html>
EOM
	exit;
}

##### 持ち物売却 ############
sub mothi_baikyaku{
	($in{'ori_ie_id'},$bangou2) = split(/_/, $in{'ori_ie_id'});
	$hausu_no = $in{'ori_ie_id'};
#	$in{'ori_ie_id'} = "$in{'ori_ie_id'}".'_'."3";

	if(!$k_id){&error("mono.cgi エラー mothimonohanbai2")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;
	close(OUT);

	$i = 0;
	foreach $data (@myitem_hairetu){
		$aitm_hiretu = (split(/<>/,$data))[0];

		$kuka_basyo = (split(/<>/,$data))[9];
		if ($kuka_basyo =~ /食料品/ and $aitm_hiretu eq "ギフト商品"){
			$aitm_hiretu = "食料品";
			&syouhin_sprit($myitem_hairetu[$i]);
			$syo_syubetu = "食料品";
			&syouhin_temp;
			$myitem_hairetu[$i] = $syo_temp;
		}
		if ($kuka_basyo =~ /ファ/ and $aitm_hiretu  eq "ギフト商品"){
			$aitm_hiretu = "ファーストフード";
			&syouhin_sprit($myitem_hairetu[$i]);
			$syo_syubetu = "ファーストフード";
			&syouhin_temp;
			$myitem_hairetu[$i] = $syo_temp;
		}
		$i++;

		if ($aitm_hiretu eq "ギフト商品"){
			push @aitem_giftsyo,$data;
		}elsif ($aitm_hiretu eq "ギフト"){ #koko2006/12/31
			push @aitem_gift,$data; #koko2006/12/31
		}else{
			push @aitem_sonota,$data;
		}
	}
	@keys0 = map {(split /<>/)[21]} @aitem_giftsyo;
	@itemgift = @aitem_giftsyo[sort {$keys0[$a] <=> $keys0[$b]} 0 .. $#keys0];
#koko2006/12/31
	@keys0 = map {(split /<>/)[21]} @aitem_gift;
	@gift = @aitem_gift[sort {$keys0[$a] <=> $keys0[$b]} 0 .. $#keys0];
#kokoend2006/12/31
	@keys0 = map {(split /<>/)[0]} @aitem_sonota;
	@itemsonota = @aitem_sonota[sort {$keys0[$a] cmp $keys0[$b]} 0 .. $#keys0];
#koko2006/12/31
	if ($gyfturi eq "yes"){
		@alldata = (@itemgift,@itemsonota,@gift);
	}else{
		@alldata = (@itemgift,@itemsonota);
	}
#kokoend2006/12/31

	if($#aitem_sonota >= $mothi_jougen){&error("オーバーです。1");} #koko2007/10/22


	&header;
	print <<"EOM";
	<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>売却したいアイテムにチェックをいれ、売却する。<br>
	※備考に（※アイコン）とある商品は、持っていることで新しいアイコンが現れます。「使用」してしまうと無くなってしまい効果も消えますのでご注意ください。<br>
	※自分で購入した「ギフト」はメール送信画面のセレクトメニューに現れます。このリストには表\示されません。<br>
	現在の$nameさんの身体エネルギー：$energy　頭脳エネルギー：$nou_energy</td>
	<td  bgcolor=#ffcc00 align=center>闇市</td>
	</tr></table><br>
	
	<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr><td colspan=26><font color=#336699>凡例：(国)＝国語up値、(数)＝数学up値、(理)＝理科up値、(社)＝社会up値、(英)＝英語up値、(音)＝音楽up値、(美)＝美術up値、（ル）=ルックスup値、（体）=体力up値、（健）=健康up値、（ス）=スピードup値、（パ）=パワーup値、（腕）=腕力up値、（脚）=脚力up値、（L）=LOVEup値、（面）=面白さup値、（H）=エッチup値<br>
	※耐久は、○回なら使用できる回数、○日なら使用できる日数です。<br>
	※カロリーは摂取できる数値です。<br>
	</font></td></tr>
		<tr bgcolor=#ccff33><td align=center nowrap>商品</td><td>売却値段</td><td align=center nowrap>残り</td><td>使用</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center nowrap>カロリー</td><td align=center>使用<br>間隔</td><td align=center>身体<br>消費</td><td align=center>頭脳<br>消費</td><!-- <td align=center nowrap>　備　考　</td> --><td align=center nowrap>購入日</td></tr>
EOM
	$now_time = time;
	@new_myitem_hairetu = ();
	$i=0;
	foreach (@alldata) {
		&syouhin_sprit($_);
		if ($syo_taikyuu_tani eq "日"){
			$keikanissuu = int (($now_time - $syo_kounyuubi) / (60*60*24));
			$nokorinissuu = $syo_taikyuu - $keikanissuu;
			if ($nokorinissuu <= 0){next;}
		}
		if ($syo_taikyuu <=0 && $syo_siyou_date + ($syo_kankaku*60) < $now_time){next;}
		if($syo_cal > 0){$calory_hyouzi = "$syo_cal kcal";}else{$calory_hyouzi = "<div align=center>ー</div>";}
		if($syo_kankaku <= 0){$syo_kankaku = "<div align=center>ー</div>";}
		if ($maeno_syo_syubetu ne "$syo_syubetu" && $syo_taikyuu > 0){
			print "<tr bgcolor=#ffff66><td colspan=26>▼$syo_syubetu</td></tr>";
		}

		if ($syo_taikyuu_tani eq "日"){
			$taikyuu_hyouzi_seikei = "$nokorinissuu日";
			$baikyaku_hyouzi = ($tanka * $nokorinissuu);
		}else{
			$taikyuu_hyouzi_seikei = "$syo_taikyuu"."$syo_taikyuu_tani";
			$baikyaku_hyouzi = ($tanka * $syo_taikyuu);
		}

		&byou_hiduke($syo_kounyuubi);

		if($syo_siyou_date + ($syo_kankaku*60) > $now_time){
			$disp_siyukanou = "－";
		}else{$disp_siyukanou = "OK";}

		if(($syo_syubetu eq "食料品" || $syo_syubetu eq "ファーストフード") && $now_time < $last_syokuzi + ($syokuzi_kankaku*60)){ 
			$disp_siyukanou = "－";
		}
		if ($oyatu_kisei eq 'yes' && $syo_syubetu eq 'アルコール' && $syo_sake > time){
			$disp_siyukanou = "－";
		}elsif ($oyatu_kisei eq 'yes' && $syo_syubetu eq 'デザート' && $syo_dezato > time){
			$disp_siyukanou = "－";
		}elsif ($oyatu_kisei eq 'yes' && $syo_syubetu eq 'ドリンク' && $syo_dorinku > time){
			$disp_siyukanou = "－";
		}
		$disp_seru = "rowspan=\"2\"";
		$disp_com = "<tr bgcolor=#cccccc><td><input type=text name=kakaku maxlength=\"9\"></td><td align=left colspan=24>【 備考 】 $syo_comment</td></tr>";
	
		if (!($syo_taikyuu <=0)){
			print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="mothi_baikyaku_do">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
	<tr bgcolor=#ccff99 align=center><td nowrap align=left $disp_seru>$i <input type=hidden value=\"$syo_hinmoku\t$syo_syubetu\" name="syo_hinmoku">$syo_hinmoku</td><td>$baikyaku_hyouzi円</td><td nowrap>$taikyuu_hyouzi_seikei</td><td>$disp_siyukanou</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right nowrap>$calory_hyouzi</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td><!-- <td align=left>$syo_comment</td> --><td nowrap>$bh_tukihi</td></tr>$disp_com
	<tr><td colspan=26>
	<div align=center>
	<input type=submit name=command value="預ける">
	<input type=submit name=command value="販売する"></div></td></form></tr>
EOM
		}
		if ($syo_taikyuu > 0){
			$maeno_syo_syubetu = "$syo_syubetu";
		}
		$i++;

	}	#foreach閉じ
	if (! @alldata){print "<tr><td colspan=26>現在所有しているアイテムはありません。</td></tr>";}
	print <<"EOM";
	</table>
	</body></html>
EOM
	&hooter("login_view","戻る");
	exit;
}


##### 売却処理 ###########
sub mothi_baikyaku_do{
	($in{'ori_ie_id'},$bangou2) = split(/_/, $in{'ori_ie_id'});
	$hausu_no = $in{'ori_ie_id'};
#	$in{'ori_ie_id'} = "$in{'ori_ie_id'}".'_'."3";

	if ($in{'syo_hinmoku'} eq ""){&error("アイテムが選ばれていません。");}
	($in_syo_hinmoku,$in_syo_syubetu) = split(/\t/,$in{'syo_hinmoku'});#2006/11/29
	if(!$k_id){&error("mono.cgi エラー mothimonohanbai3")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;
	close(OUT);
	$siyouzumi_flag = 0;
#	if(@alldata >= $mothi_jougen){&error("オーバーです。2");}
	if ($in{'kakaku'} < 0){&error("マイナス設定は出来ません。");}

	foreach  (@myitem_hairetu) {
		&syouhin_sprit2($_);
		if($syo_hinmoku eq $in_syo_hinmoku && $syo_syubetu eq $in_syo_syubetu && !$furagu){
			$now_time = time;
			if ($now_time < $syo_kounyuubi + $uritobasi_kisei){
				$print_messe .= "●$in_syo_hinmokuの売却は未だ出来ません。";
			}else{
				if ($syo_taikyuu_tani eq "日"){
					$keikanissuu = int (($now_time - $syo_kounyuubi) / (60*60*24));
					$nokorinissuu = $syo_taikyuu - $keikanissuu;
					$baikyaku_hyouzi = ($tanka * $nokorinissuu);
					if ($baikyaku_hyouzi > $uritobasi_jyougen){
						$baikyaku_hyouzi = $uritobasi_jyougen;
						$tanka = int($baikyaku_hyouzi / $nokorinissuu);
					}
#koko2007/01/01
					if ($keikanissuu == 0){&error('日数が1日経過していませんのでこの商品はお取り扱い出来ません。');}
					$syo_kounyuubi = $now_time;
					$syo_taikyuu = $nokorinissuu;
#kokoend
				}else{
					$baikyaku_hyouzi = ($tanka * $syo_taikyuu);
					if ($baikyaku_hyouzi > $uritobasi_jyougen){
						$baikyaku_hyouzi = $uritobasi_jyougen;
					}

					$tanka = int($baikyaku_hyouzi / $syo_taikyuu);
				}

				if ($baikyaku_hyouzi > $uritobasi_jyougen){
					$baikyaku_hyouzi = $uritobasi_jyougen;
				}

				if($syo_syubetu eq 'ギフト商品'){
					$syo_comment_t = $syo_comment;
					($syo_comment)= split(/。/,$syo_comment_t);
					$syo_comment .="。";
				}
				$syo_kounyuubi = time;
				$furagu = 1;

				if ($in{'kakaku'}){
					$syo_nedan = $in{'kakaku'};
				}

				if ($in{'command'} eq '預ける'){
					$zokusei = 1;
				}

				#商品に入れる
				$mothi_log_f = "./member/$k_id/3_log.cgi";
				open(IN,"< $mothi_log_f") || &error("Open Error : $mothi_log_f");
				eval{ flock (IN, 1); };
				$my_para = <IN>;
				@mothi_dat = <IN>;
				close(IN);

				if(@mothi_dat >= $mothi_jougen){&error("オーバーです。3");}
				&syouhin_temp2;
				unshift (@mothi_dat,$syo_temp2);

				open(OUT,">$mothi_log_f") || &error("Write Error : $mothi_log_f");
				eval{ flock (OUT, 2); };
				print OUT $my_para;
				print OUT @mothi_dat;
				close(OUT);	

			#	$money += $baikyaku_hyouzi;
				$print_messe .= "●$in_syo_hinmokuを操作しました。";#koko2006/11/29
				next;
			}		
		}#if（「売却」コマンドだった場合）の閉じ
		
		if ($syo_taikyuu <= 0 && $syo_siyou_date + ($syo_kankaku*60) < $now_time){next;}
		&syouhin_temp2;
		push (@new_myitem_hairetu,$syo_temp2);
	}	#foreachの閉じ

#ログ更新
#	&temp_routin;
#	&log_kousin($my_log_file,$k_temp);
			
#自分の所有物ファイルを更新
	&lock;
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_hairetu;
	close(OUT);	
#koko2006/11/02
	&unlock;
			
	&header;
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
	<span class="job_messe">
	$print_messe
	</span>
	</td></tr></table>
	<br>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="mothi_baikyaku">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
	<input type=hidden name=shiyori value="kau">
	<input type=submit value="続けて売る/預ける"></form>

<!-- <div align="center"><a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div> -->
	<form method=POST action="$script">
	<input type=hidden name=mode value="login_view">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="戻る">
	</form></div>

	</body></html>
EOM
	exit;
}



