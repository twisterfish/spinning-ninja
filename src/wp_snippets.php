<?php
    global $wpdb;
    $wpdb ->show_errors();

    echo "<table style=\"font-family: arial, sans-serif; border-collapse: collapse;width: 100%;\">
        <thead>
            <tr style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">
   
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Date Played</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Track Name</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Artist Name</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Album Name</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Date Added</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Track Length</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Number of Plays</th>
                <th style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">Beats Per Minute</th>
            </tr>
        </thead>
        <tbody>";
            $tracks = $wpdb->get_results("SELECT * FROM spin_playlists"); 
            foreach ($tracks as $track) {
                echo "<tr>
                    <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->date_played . "</td>
                    <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->track_name . "</td>
                    <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->artist_name . "</td>
                    <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->album_name . "</td>
                    <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->date_added . "</td>
                    <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->track_length . "</td>
                    <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->num_plays . "</td>
                    <td style=\"border: 1px solid #dddddd; text-align: left; padding: 8px;\">" . $track->beats_per_minute . "</td>
                </tr>";
            }
        echo "</tbody></table>";