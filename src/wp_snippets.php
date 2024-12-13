<?php
global $wpdb;
$wpdb->show_errors();

echo "<h1>Malcolm's Tracks</h1>";

echo " <table style=\"font-family: arial, sans-serif; border-collapse: collapse; width: 100%;\">";
echo "  <thead>
            <tr style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;background-color: #f2f3fc;\">
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Date Played</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Track Name</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Artist Name</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Album Name</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Track Length</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Number of Plays</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Beats Per Minute</th>
            </tr>
        </thead>
        <tbody>";

$tracks = $wpdb->get_results("SELECT * FROM spin_playlists ORDER BY date_played DESC");
$oddEven = true;
foreach ($tracks as $track) {

    if ($oddEven) {
        echo "<tr style=\"background-color: #f2f2f2;\">";
        $oddEven = false;
    } else {
        echo "<tr style=\"background-color: #c9bdbd;\">";
        $oddEven = true;
    }

    echo "
            <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . date("F j, Y", strtotime($track->date_played)) . "</td>
            <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->track_name . "</td>
            <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->artist_name . "</td>
            <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->album_name . "</td>
            <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->track_length . "</td>
            <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->num_plays . "</td>
            <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->beats_per_minute . "</td>
        </tr>";
}

echo "</tbody></table>";
