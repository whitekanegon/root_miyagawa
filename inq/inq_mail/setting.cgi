#======================================================================================
#	基本メールフォーム　v1.0　Directed By PenguinNoise J.KANEDA
#
#   ■各種設定
#======================================================================================

#------------------------------------------------------------------------------
# Perlライブラリ
#------------------------------------------------------------------------------
$lib  = './lib';
$cgilib = './cgi-lib.pl';

#------------------------------------------------------------------------------
# 基本設定
#------------------------------------------------------------------------------

#管理用CGI
$admin_script = './admin.cgi';

#パスワード
$passwd = 'miyagawainq';

#------------------------------------------------------------------------------
# データベースファイル指定
#------------------------------------------------------------------------------

#↓管理ページ用

#データベースディレクトリ
$db_dr = './db';

#基本情報
$db_kihon = "$db_dr/kihon.dat";

#通知（管理者宛）メール
$db_mail_admin = "$db_dr/mail_admin.dat";

#確認（者宛）メール
$db_mail_henshin = "$db_dr/mail_henshin.dat";

#↓フォーム用

#データ
$db_user = "$db_dr/user.dat";

#------------------------------------------------------------------------------
# スキンファイル指定
#------------------------------------------------------------------------------

#↓管理ページ用

#スキンディレクトリ
$skin_admin_dir = './skin_admin';

#トップ
$skin_top = "$skin_admin_dir/skin_top.html";

#基本情報
$skin_kihon = "$skin_admin_dir/skin_kihon.html";

#通知（管理者宛）メール
$skin_mail_admin = "$skin_admin_dir/skin_mail_admin.html";

#確認（者宛）メール
$skin_mail_henshin = "$skin_admin_dir/skin_mail_henshin.html";

#設定完了
$skin_kanryo = "$skin_admin_dir/skin_kanryo.html";

#入室
$skin_pass = "$skin_admin_dir/skin_pass.html";

#↓フォーム用

#確認画面
$skin_check = './check_skin.html';

#エラー画面
$skin_error = './error_skin.html';


#------------------------------------------------------------------------------
# デコード
#------------------------------------------------------------------------------
sub decode {
	local($key,$val);
	undef(%in);

	&ReadParse;
	
	while ( ($key,$val) = each(%in) ) {
		
		# シフトJISコード変換
		Jcode::convert(\$val, 'utf8');

		# 不要コード排除
		
		$val =~ s/&([^aqLGlg]{1,1})/&amp;$1/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/<>/&LT;&GT;/g;
		$val =~ s/<([^b]{1,1})/&lt;$1/g;
		$val =~ s/([^r]{1,1})>/$1&gt;/g;
		$val =~ s/\r\n/<br>/g;
		$val =~ s/\r/<br>/g;
		$val =~ s/\n/<br>/g;
		$val =~ s/\r//g;
		$val =~ s/\n//g;
		$val =~ s/\*/＊/g;
		$val =~ s/\,/、/g;
		
		$in{$key} = $val;
		
	}
	$mode = $in{'mode'};
	$regist = $in{'regist'};
	$back_mode = $in{'back_mode'};
	$passwd_form = $in{'passwd'};
	$email = $in{'email'};

}

#------------------------------------------------------------------------------
# データベース読み込み
#------------------------------------------------------------------------------

#基本情報
sub open_kihon{
	open(IN,"$db_kihon") || &error("$db_kihonが開けません。");
	while(<IN>){
		($mailto_1,$mailto_2,$mailto_3,$kanryo_url,$sendmail_pas,$henshin_sign) = split(/<>/);
	}
	close(IN);
}


#------------------------------------------------------------------------------
# 時間処理
#------------------------------------------------------------------------------

sub times {
	($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	@w_j = ('日','月','火','水','木','金','土');
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	# 日時のフォーマット
	$date1 = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
			$year+1900,$mon+1,$mday,$w_j[$wday],$hour,$min);
	$date2 = sprintf("%s, %02d %s %04d %02d:%02d:%02d",
			$w[$wday],$mday,$m[$mon],$year+1900,$hour,$min,$sec) . " +0900";
	$date3 = sprintf("%02d%02d%02d%02d%02d",
			$mon+1,$mday,$hour,$min,$sec);
	
	$su_year = $year;
	$year = $year + 1900;

	return ($date1,$date2);
}

#------------------------------------------------------------------------------
# ヘッダー
#------------------------------------------------------------------------------
sub header{

	print "Content-type: text/html\n\n";

}

#------------------------------------------------------------------------------
# エラー処理
#------------------------------------------------------------------------------
sub error{

	&header;
	print <<"EOF";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<title>チケット予\約システム　管理ページ &gt; エラー！</title>
<link href="base.css" rel="stylesheet" type="text/css">
</head>

<body bgcolor="#FFFFFF">
<div align="center">
<span class="L"><font color="#CC0000">■エラー！■</font></span>
<br>
<br>
 	<span class="M">$_[0]</span>
  <br>
  <br>
  <hr>
		<form>
  <input type="button" name="Submit" value="戻る" onclick="history.back()">
		</form>
</div>
EOF
exit;
}

#------------------------------------------------------------------------------
# エラー処理（フォーム用）
#------------------------------------------------------------------------------
sub error_form{
	open(IN,"$skin_error") || &error("$skin_errorが開けません。");
	&header;
	while(<IN>){
		#スキンファイルにSSI記述がある場合
		if(/#include/){
			@kaiso = split(/\//,$ENV{'REQUEST_URI'});
			$kaiso = "";
			foreach (0 .. $#kaiso - 2){
				$kaiso .= "../";
			}
			($dummy1,$ssi_file,$dummy2) = split(/"/);
			$include_path = $kaiso.$ssi_file;
			open(INCLUDE,"$include_path") || &error_form("$include_pathが開けません。");
			while($inc_line = <INCLUDE>){
				Jcode::convert(\$inc_line, 'utf8');
				print $inc_line;
			}
			close(INCLUDE);
			next;
		}

		s/\$error_msg/$_[0]/;
		s/!play_org!/$play_org/g;
		s/!play_name!/$play_name/g;
		
		# シフトJISコード変換
		Jcode::convert(\$_, 'utf8');
		
		print "$_";
	}
	close(IN);
	exit;
}

#------------------------------------------------------------------------------
# 入室画面（パスワード入力）
#------------------------------------------------------------------------------
sub passwd{
	open(IN,"$skin_pass") || &error("$skin_passが開けません。");
	&header;
	while(<IN>){
		s/!msg!/$_[0]/;
		$_ =~ s/\$admin_script/$admin_script/g;
		
		# シフトJISコード変換
		Jcode::convert(\$_, 'utf8');
		
		print "$_";
	}
	close(IN);
	exit;
}


#------------------------------------------------------------------------------
#  BASE64変換
#------------------------------------------------------------------------------
sub base64 {
	local($sub) = $_[0];
	Jcode::convert(\$sub, 'jis', 'utf8');

	$sub =~ s/\x1b\x28\x42/\x1b\x28\x4a/g;
	$sub = "=?iso-2022-jp?B?" . &b64enc($sub) . "?=";
	$sub;
}
sub b64enc {
	local($ch)="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	local($x, $y, $z, $i);
	$x = unpack("B*", $_[0]);
	for ($i=0; $y=substr($x,$i,6); $i+=6) {
		$z .= substr($ch, ord(pack("B*", "00" . $y)), 1);
		if (length($y) == 2) {
			$z .= "==";
		} elsif (length($y) == 4) {
			$z .= "=";
		}
	}
	$z;
}

#------------------------------------------------------------------------------
#  ホスト取得
#------------------------------------------------------------------------------
sub get_host {
	local($host,$addr);

	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}
	if($host= "") { $host = $addr; }
}

#------------------------------------------------------------------------------
#  クッキー発行
#------------------------------------------------------------------------------
sub set_cookie {
	local(@cook) = @_;
	local($gmt, $cook, @t, @m, @w);

	@t = gmtime(time + 60*24*60*60);
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# 国際標準時を定義
	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);

	# 保存データをURLエンコード
	$cook='';
	foreach (@cook) {
		s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
		$cook .= "$_<>";
	}

	# 格納
	print "Set-Cookie: TICKET_SYSTEM=$cook; expires=$gmt\n";
}

#------------------------------------------------------------------------------
#  クッキー取得
#------------------------------------------------------------------------------
sub get_cookie {
	local($key, $val, *cook);

	# クッキーを取得
	$cook = $ENV{'HTTP_COOKIE'};

	# 該当IDを取り出す
	foreach ( split(/;/, $cook) ) {
		($key, $val) = split(/=/);
		$key =~ s/\s//g;
		$cook{$key} = $val;
	}

	# データをURLデコードして復元
	@cook=();
	foreach ( split(/<>/, $cook{'TICKET_SYSTEM'}) ) {
		s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("H2", $1)/eg;

		push(@cook,$_);
	}
	return (@cook);
}

1;