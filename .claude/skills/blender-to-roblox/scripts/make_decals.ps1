Add-Type -AssemblyName System.Drawing
$out = 'D:\god\exports\decals\factory'
New-Item -ItemType Directory -Force $out | Out-Null
$rng = New-Object System.Random 1234

function New-Canvas($w, $h) {
  $bmp = New-Object System.Drawing.Bitmap($w, $h, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.SmoothingMode = 'AntiAlias'; $g.TextRenderingHint = 'AntiAliasGridFit'; $g.Clear([System.Drawing.Color]::Transparent)
  return @($bmp, $g)
}
function C($a, $r, $g, $b) { [System.Drawing.Color]::FromArgb($a, $r, $g, $b) }
function Brush($col) { New-Object System.Drawing.SolidBrush($col) }
function Font($name, $size, $style = 'Bold') { New-Object System.Drawing.Font($name, [single]$size, [System.Drawing.FontStyle]$style, [System.Drawing.GraphicsUnit]::Pixel) }
function CenterText($g, $text, $font, $brush, $cx, $cy) {
  $sz = $g.MeasureString($text, $font)
  $g.DrawString($text, $font, $brush, [single]($cx - $sz.Width / 2), [single]($cy - $sz.Height / 2))
}
# weathering: erase random flecks / scratches (alpha), add rust streaks and grime
function FitFont($g, $text, $name, $size, $maxW, $style = 'Bold') {
  $f = Font $name $size $style
  while ($g.MeasureString($text, $f).Width -gt $maxW -and $size -gt 10) { $size -= 2; $f = Font $name $size $style }
  return $f
}
function EraseAt($bmp, $x, $y, $keep) {
  if ($x -ge 0 -and $y -ge 0 -and $x -lt $bmp.Width -and $y -lt $bmp.Height) {
    $c = $bmp.GetPixel($x, $y)
    if ($c.A -gt 0) { $bmp.SetPixel($x, $y, [System.Drawing.Color]::FromArgb([int]($c.A * $keep), $c.R, $c.G, $c.B)) }
  }
}
function Weather($bmp, $g, $amount, $rust) {
  $w = $bmp.Width; $h = $bmp.Height
  # paint chips: irregular clusters near the edges and a few inside
  for ($i = 0; $i -lt [int](40 * $amount); $i++) {
    if ($rng.NextDouble() -lt 0.7) {
      $side = $rng.Next(0, 4)
      if ($side -eq 0) { $x = $rng.Next(0, $w); $y = $rng.Next(0, 24) } elseif ($side -eq 1) { $x = $rng.Next(0, $w); $y = $h - $rng.Next(1, 24) }
      elseif ($side -eq 2) { $x = $rng.Next(0, 24); $y = $rng.Next(0, $h) } else { $x = $w - $rng.Next(1, 24); $y = $rng.Next(0, $h) }
    } else { $x = $rng.Next(0, $w); $y = $rng.Next(0, $h) }
    $n = $rng.Next(6, 30)
    for ($k = 0; $k -lt $n; $k++) {
      $cx = $x + $rng.Next(-14, 15); $cy = $y + $rng.Next(-9, 10); $r = $rng.Next(1, 4)
      for ($dx = -$r; $dx -le $r; $dx++) { for ($dy = -$r; $dy -le $r; $dy++) { if ($dx * $dx + $dy * $dy -le $r * $r) { EraseAt $bmp ($cx + $dx) ($cy + $dy) 0.1 } } }
    }
  }
  # scratches
  for ($i = 0; $i -lt [int](25 * $amount); $i++) {
    $x = $rng.Next(0, $w); $y = $rng.Next(0, $h); $len = $rng.Next(20, 120); $ang = $rng.NextDouble() * 3.14
    for ($t = 0; $t -lt $len; $t++) { EraseAt $bmp ([int]($x + [math]::Cos($ang) * $t)) ([int]($y + [math]::Sin($ang) * $t)) 0.35 }
  }
  if ($rust) {
    for ($i = 0; $i -lt 14; $i++) {
      $x = $rng.Next(10, $w - 10); $len = $rng.Next([int]($h * 0.2), [int]($h * 0.8))
      $pen = New-Object System.Drawing.Pen((C 70 110 60 35), [single]$rng.Next(3, 10))
      $g.DrawLine($pen, [single]$x, [single]$rng.Next(0, [int]($h * 0.3)), [single]($x + $rng.Next(-6, 6)), [single]$len)
    }
    $grime = Brush (C 45 60 52 40)
    for ($i = 0; $i -lt 40; $i++) { $g.FillEllipse($grime, $rng.Next(0, $w), $rng.Next(0, $h), $rng.Next(10, 60), $rng.Next(6, 30)) }
  }
}
function Save($bmp, $g, $name) { $g.Dispose(); $bmp.Save("$out\$name.png", [System.Drawing.Imaging.ImageFormat]::Png); $bmp.Dispose(); "saved $name" }

# ---------- building name plates (blue enamel, white letters) ----------
function Plate($name, $line1, $line2) {
  $c = New-Canvas 1024 256; $bmp = $c[0]; $g = $c[1]
  $g.FillRectangle((Brush (C 255 28 52 92)), 6, 6, 1012, 244)
  $pen = New-Object System.Drawing.Pen((C 255 220 222 214), 8); $g.DrawRectangle($pen, 18, 18, 988, 220)
  CenterText $g $line1 (FitFont $g $line1 'Arial Black' 92 920) (Brush (C 255 232 232 224)) 512 ($(if ($line2) { 100 } else { 128 }))
  if ($line2) { CenterText $g $line2 (FitFont $g $line2 'Arial' 44 900) (Brush (C 255 210 212 205)) 512 190 }
  foreach ($p in @(@(36, 36), @(988, 36), @(36, 220), @(988, 220))) { $g.FillEllipse((Brush (C 255 120 120 118)), $p[0] - 8, $p[1] - 8, 16, 16) }
  Weather $bmp $g 1.0 $true
  Save $bmp $g $name
}
Plate 'SIGN_BlastFurnace' 'BLAST FURNACE No.1' 'IRONMAKING DIVISION'
Plate 'SIGN_RollingMill' 'HOT STRIP MILL' 'BAY 2 - ROLLING'
Plate 'SIGN_PowerStation' 'POWER STATION' 'TURBINE HALL  B'
Plate 'SIGN_CokeOvens' 'COKE OVEN BATTERY 3' 'BY-PRODUCTS PLANT'
Plate 'SIGN_GasHolder' 'GAS HOLDER G-1' 'BLAST FURNACE GAS'
Plate 'SIGN_Weighbridge' 'WEIGHBRIDGE' 'ALL TRUCKS STOP HERE'

# ---------- hazard signs (portrait 512x640) ----------
function Hazard($name, $kind, $head, $l1, $l2) {
  $c = New-Canvas 512 640; $bmp = $c[0]; $g = $c[1]
  $g.FillRectangle((Brush (C 255 236 232 220)), 8, 8, 496, 624)
  if ($kind -eq 'danger') {
    $g.FillRectangle((Brush (C 255 18 18 18)), 8, 8, 496, 150)
    $g.FillEllipse((Brush (C 255 196 30 34)), 66, 28, 380, 110)
    CenterText $g $head (Font 'Arial Black' 70) (Brush (C 255 245 245 240)) 256 84
  } else {
    $g.FillRectangle((Brush (C 255 232 182 28)), 8, 8, 496, 150)
    CenterText $g $head (Font 'Arial Black' 70) (Brush (C 255 18 18 18)) 256 84
  }
  # icon area
  $tri = [System.Drawing.PointF[]]@((New-Object System.Drawing.PointF(256, 186)), (New-Object System.Drawing.PointF(400, 420)), (New-Object System.Drawing.PointF(112, 420)))
  if ($kind -eq 'noentry') {
    $g.FillEllipse((Brush (C 255 196 30 34)), 146, 196, 220, 220); $g.FillRectangle((Brush (C 255 245 245 240)), 176, 288, 160, 36)
  } elseif ($kind -eq 'hardhat') {
    $g.FillEllipse((Brush (C 255 30 70 150)), 146, 196, 220, 220)
    $g.FillPie((Brush (C 255 245 245 240)), 186, 246, 140, 120, 180, 180); $g.FillRectangle((Brush (C 255 245 245 240)), 176, 302, 160, 18)
  } else {
    $g.FillPolygon((Brush (C 255 232 182 28)), $tri)
    $pen = New-Object System.Drawing.Pen((C 255 18 18 18), 14); $g.DrawPolygon($pen, $tri)
    if ($kind -eq 'danger') {
      $bolt = [System.Drawing.PointF[]]@((New-Object System.Drawing.PointF(270, 250)), (New-Object System.Drawing.PointF(222, 335)), (New-Object System.Drawing.PointF(258, 335)), (New-Object System.Drawing.PointF(236, 405)), (New-Object System.Drawing.PointF(296, 310)), (New-Object System.Drawing.PointF(260, 310)), (New-Object System.Drawing.PointF(286, 250)))
      $g.FillPolygon((Brush (C 255 18 18 18)), $bolt)
    } else { CenterText $g '!' (Font 'Arial Black' 130) (Brush (C 255 18 18 18)) 256 340 }
  }
  CenterText $g $l1 (FitFont $g $l1 'Arial Black' 52 460) (Brush (C 255 20 20 20)) 256 488
  CenterText $g $l2 (FitFont $g $l2 'Arial' 38 460) (Brush (C 255 30 30 30)) 256 566
  Weather $bmp $g 1.3 $true
  Save $bmp $g $name
}
Hazard 'HAZ_HighVoltage' 'danger' 'DANGER' 'HIGH VOLTAGE' 'KEEP OUT'
Hazard 'HAZ_Gas' 'warning' 'WARNING' 'CO GAS AREA' 'NO SMOKING'
Hazard 'HAZ_HotMetal' 'warning' 'CAUTION' 'MOLTEN METAL' 'STAY BEHIND LINE'
Hazard 'HAZ_NoEntry' 'noentry' 'DANGER' 'NO ENTRY' 'AUTHORISED ONLY'
Hazard 'HAZ_HardHat' 'hardhat' 'NOTICE' 'HARD HAT AREA' 'AT ALL TIMES'

# ---------- directional sign ----------
$c = New-Canvas 1024 384; $bmp = $c[0]; $g = $c[1]
$g.FillRectangle((Brush (C 255 30 96 60)), 6, 6, 1012, 372)
$pen = New-Object System.Drawing.Pen((C 255 230 230 222), 6); $g.DrawRectangle($pen, 18, 18, 988, 348)
$g.DrawLine($pen, 18, 192, 1006, 192)
$fnt = Font 'Arial Black' 64; $w = Brush (C 255 236 236 228)
$g.DrawString([string][char]0x2190 + ' BLAST FURNACE', $fnt, $w, 40, 50)
$g.DrawString('POWER STATION ' + [string][char]0x2192, $fnt, $w, 260, 230)
Weather $bmp $g 1.0 $true
Save $bmp $g 'SIGN_Direction'

# ---------- floor stencil ----------
$c = New-Canvas 1024 512; $bmp = $c[0]; $g = $c[1]
$y = Brush (C 235 222 176 34)
for ($i = 0; $i -lt 9; $i++) { $pts = [System.Drawing.PointF[]]@((New-Object System.Drawing.PointF(($i * 120 - 40), 0)), (New-Object System.Drawing.PointF(($i * 120 + 20), 0)), (New-Object System.Drawing.PointF(($i * 120 - 40 + 60 - 60), 120)), (New-Object System.Drawing.PointF(($i * 120 - 100), 120))); $g.FillPolygon($y, $pts) }
CenterText $g 'KEEP CLEAR' (Font 'Arial Black' 150) $y 512 300
$g.FillRectangle($y, 0, 440, 1024, 40)
Weather $bmp $g 2.2 $false
Save $bmp $g 'FLOOR_KeepClear'

# ---------- spray graffiti ----------
function Spray($g, $text, $font, $col, $x, $y, $drips) {
  for ($k = 0; $k -lt 6; $k++) {
    $b = Brush ([System.Drawing.Color]::FromArgb(45, $col.R, $col.G, $col.B))
    $g.DrawString($text, $font, $b, [single]($x + $rng.Next(-3, 4)), [single]($y + $rng.Next(-3, 4)))
  }
  $g.DrawString($text, $font, (Brush $col), [single]$x, [single]$y)
  $sz = $g.MeasureString($text, $font)
  for ($d = 0; $d -lt $drips; $d++) {
    $dx = $x + $rng.Next(20, [int]$sz.Width - 20); $dy = $y + $sz.Height * 0.78
    $len = $rng.Next(15, 90)
    $pen = New-Object System.Drawing.Pen(([System.Drawing.Color]::FromArgb(200, $col.R, $col.G, $col.B)), [single]$rng.Next(3, 7))
    $g.DrawLine($pen, [single]$dx, [single]$dy, [single]$dx, [single]($dy + $len))
    $g.FillEllipse((Brush $col), [single]($dx - 4), [single]($dy + $len - 3), 8, 9)
  }
}
$red = C 235 178 28 26; $white = C 235 226 224 214; $blk = C 240 22 22 22; $yel = C 235 214 170 30
$c = New-Canvas 1024 512; $bmp = $c[0]; $g = $c[1]
Spray $g 'WE ARE STILL' (Font 'Impact' 150 'Regular') $red 40 20 7
Spray $g 'INSIDE' (Font 'Impact' 170 'Regular') $red 230 190 6
Spray $g '6 OF US - SHIFT B' (Font 'Impact' 60 'Regular') $white 330 410 2
Save $bmp $g 'GR_StillInside'

$c = New-Canvas 1024 512; $bmp = $c[0]; $g = $c[1]
Spray $g "DON'T GO NORTH" (Font 'Impact' 140 'Regular') $red 30 20 8
Spray $g 'IT LIVES IN THE SCRAP YARD' (Font 'Impact' 72 'Regular') $white 60 220 3
$pen = New-Object System.Drawing.Pen($red, 26); $pen.EndCap = 'ArrowAnchor'
$g.DrawLine($pen, 512, 480, 512, 335)
Save $bmp $g 'GR_DontGoNorth'

$c = New-Canvas 1024 512; $bmp = $c[0]; $g = $c[1]
Spray $g 'DAY 112' (Font 'Impact' 120 'Regular') $white 40 20 3
$pen = New-Object System.Drawing.Pen($white, 9)
for ($grp = 0; $grp -lt 15; $grp++) {
  $gx = 60 + ($grp % 5) * 190; $gy = 175 + [math]::Floor($grp / 5) * 108
  for ($k = 0; $k -lt 4; $k++) { $g.DrawLine($pen, [single]($gx + $k * 26), [single]$gy, [single]($gx + $k * 26 + $rng.Next(-5, 6)), [single]($gy + 85)) }
  if ($grp -lt 14) { $g.DrawLine($pen, [single]($gx - 14), [single]($gy + 78), [single]($gx + 96), [single]($gy + 8)) }
}
Save $bmp $g 'GR_Day112'

$c = New-Canvas 1024 512; $bmp = $c[0]; $g = $c[1]
Spray $g 'MINA -' (Font 'Impact' 110 'Regular') $yel 40 30 4
Spray $g 'DAD IS AT THE FURNACE' (Font 'Impact' 90 'Regular') $yel 40 170 5
Spray $g 'WAIT FOR ME' (Font 'Impact' 110 'Regular') $yel 220 310 4
Save $bmp $g 'GR_Mina'

$c = New-Canvas 1024 1024; $bmp = $c[0]; $g = $c[1]
Spray $g 'SOS' (Font 'Impact' 520 'Regular') $white 90 140 0
Save $bmp $g 'GR_SOS'

$c = New-Canvas 512 512; $bmp = $c[0]; $g = $c[1]
Spray $g 'WATER' (Font 'Impact' 120 'Regular') $blk 70 60 2
$pen = New-Object System.Drawing.Pen($blk, 30); $pen.EndCap = 'ArrowAnchor'
$g.DrawLine($pen, 90, 330, 430, 330)
Spray $g 'CLEAN - BOIL IT' (Font 'Impact' 48 'Regular') $blk 90 400 1
Save $bmp $g 'GR_Water'

