
                CREATE TABLE IF NOT EXISTS project_0 (
                    id INT PRIMARY KEY,
                    project_url_date DATE,
                    project_url VARCHAR(255),
                    begin_at TIME,
                    end_at TIME,
                    total_time TIME,
                    links_parent_id INT
                );
            
                        INSERT INTO project_0 (id, project_url_date, project_url, begin_at, end_at, total_time, links_parent_id)
                        VALUES (0, '2023-07-13', 'https://projects.intra.42.fr/projects/cpp-module-09/projects_users/3167865', '13:15:00', '14:09:46', '00:54:46', 0);
                    
                        INSERT INTO project_0 (id, project_url_date, project_url, begin_at, end_at, total_time, links_parent_id)
                        VALUES (1, '2023-07-11', 'https://projects.intra.42.fr/projects/42cursus-ft_printf/projects_users/3135549', '17:30:00', '17:46:28', '00:16:28', 0);
                    