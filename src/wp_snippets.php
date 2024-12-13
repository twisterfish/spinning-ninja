<?php
    global $wpdb;
    $wpdb ->show_errors();
    $tracks = $wpdb->get_results("SELECT * FROM spin_playlists ORDER BY date_played DESC");
    echo "<h2>Malcolm's Playlist for " . $tracks[1]->date_played . "</h2>";

    echo "
    <table style=\"font-family: arial, sans-serif; border-collapse: collapse;width: 100%;\">
        <thead>
            <tr style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Track Name</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Artist Name</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Album Name</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Track Length</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Number of Plays</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Beats Per Minute</th>
            </tr>
        </thead>
        <tbody>";
            //$tracks = $wpdb->get_results("SELECT * FROM spin_playlists ORDER BY date_played DESC"); 
            foreach ($tracks as $track) {
                echo "<tr>
                    <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->track_name . "</td>
                    <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->artist_name . "</td>
                    <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->album_name . "</td>
                    <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->track_length . "</td>
                    <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->num_plays . "</td>
                    <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->beats_per_minute . "</td>
                </tr>";
            }
    echo "</tbody></table>";