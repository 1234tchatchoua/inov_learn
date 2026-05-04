-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : lun. 04 mai 2026 à 07:57
-- Version du serveur : 10.6.25-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `inov`
--

-- --------------------------------------------------------

--
-- Structure de la table `accueil_admin`
--

CREATE TABLE `accueil_admin` (
  `id` bigint(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `accueil_admin`
--

INSERT INTO `accueil_admin` (`id`, `email`, `password`, `role`) VALUES
(1, 'inovlearn@123.com', 'fdcbd22964851e47f38d17d2485d573c90ea26fb119dca69fa4d04bf593b646f', 'admin');

-- --------------------------------------------------------

--
-- Structure de la table `accueil_cours`
--

CREATE TABLE `accueil_cours` (
  `id` bigint(20) NOT NULL,
  `nom` varchar(150) NOT NULL,
  `code` varchar(50) NOT NULL,
  `enseignant_id` bigint(20) NOT NULL,
  `filiere_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `accueil_cours`
--

INSERT INTO `accueil_cours` (`id`, `nom`, `code`, `enseignant_id`, `filiere_id`) VALUES
(4, 'JAVASCRIPT', 'CRS902', 2, 6),
(5, 'CSS', 'CRS346', 2, 6),
(6, 'F2', 'CRS781', 4, 4);

-- --------------------------------------------------------

--
-- Structure de la table `accueil_emploidutemps`
--

CREATE TABLE `accueil_emploidutemps` (
  `id` bigint(20) NOT NULL,
  `date` date NOT NULL,
  `heure_debut` time(6) NOT NULL,
  `heure_fin` time(6) NOT NULL,
  `cours_id` bigint(20) NOT NULL,
  `enseignant_id` bigint(20) NOT NULL,
  `filiere_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `accueil_emploidutemps`
--

INSERT INTO `accueil_emploidutemps` (`id`, `date`, `heure_debut`, `heure_fin`, `cours_id`, `enseignant_id`, `filiere_id`) VALUES
(2, '2026-04-08', '08:30:00.000000', '18:00:00.000000', 4, 2, 6),
(3, '2026-04-27', '10:00:00.000000', '16:22:00.000000', 4, 3, 6),
(4, '2026-04-28', '10:47:00.000000', '16:47:00.000000', 5, 4, 4),
(5, '2026-04-28', '09:55:00.000000', '18:55:00.000000', 6, 4, 4);

-- --------------------------------------------------------

--
-- Structure de la table `accueil_enseignant`
--

CREATE TABLE `accueil_enseignant` (
  `id` bigint(20) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) DEFAULT NULL,
  `telephone` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(255) NOT NULL,
  `date_naissance` date NOT NULL,
  `sexe` varchar(1) NOT NULL,
  `adresse` varchar(200) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `role` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `accueil_enseignant`
--

INSERT INTO `accueil_enseignant` (`id`, `nom`, `prenom`, `telephone`, `email`, `password`, `date_naissance`, `sexe`, `adresse`, `photo`, `role`) VALUES
(2, 'NKOUEBO', 'PEGUY', '678563771', 'peguy@gmail.com', 'fdcbd22964851e47f38d17d2485d573c90ea26fb119dca69fa4d04bf593b646f', '2002-02-23', 'M', 'MAKEPE', '', 'teacher'),
(3, 'NOULA ', 'PASCAL', '674356789', 'pascal@gmail.com', '4fa931de7524207b065a17acf54bb900dde5f69ee1b9c2c754890ffb0e07a9d8', '1996-06-07', 'M', 'NDOKOTI', '', 'teacher'),
(4, 'BAYE', 'HERMAN', '673456789', 'herman123@gmail.com', '2808b7b0ddf313bc951d58e3d0f975443fdc9304adec8d454e2bbdf058f9bb3a', '1999-05-03', 'M', 'NDOKOTI', '', 'teacher');

-- --------------------------------------------------------

--
-- Structure de la table `accueil_evaluation`
--

CREATE TABLE `accueil_evaluation` (
  `id` bigint(20) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `coefficient` double NOT NULL,
  `cours_id` bigint(20) NOT NULL,
  `filiere_id` bigint(20) NOT NULL,
  `sequence` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `accueil_evaluation`
--

INSERT INTO `accueil_evaluation` (`id`, `nom`, `coefficient`, `cours_id`, `filiere_id`, `sequence`) VALUES
(1, 'SEQUENCE 1', 1, 5, 6, 'S1'),
(2, 'Evaluation Maths S1', 6, 4, 6, 'S1'),
(3, 'COMPTA', 2, 5, 3, 'S1'),
(4, 'controle continu 2', 6, 4, 6, 'S2');

-- --------------------------------------------------------

--
-- Structure de la table `accueil_filiere`
--

CREATE TABLE `accueil_filiere` (
  `id` bigint(20) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `duree` int(10) UNSIGNED NOT NULL CHECK (`duree` >= 0),
  `frais_total` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `accueil_filiere`
--

INSERT INTO `accueil_filiere` (`id`, `nom`, `duree`, `frais_total`) VALUES
(3, 'Secrétariat Bureautique', 10, 350000.00),
(4, 'Fiscalité', 12, 300000.00),
(5, 'Graphisme production', 9, 325000.00),
(6, 'Développement web', 12, 400000.00),
(7, 'Maintenance informatique et réseau', 9, 450000.00),
(8, 'Maintenance informatique', 4, 350000.00),
(9, 'Administration système', 4, 235000.00),
(10, 'Comptabilité de gestion', 12, 400000.00),
(11, 'Marketing digital', 6, 325000.00),
(12, 'Marketing', 12, 375000.00);

-- --------------------------------------------------------

--
-- Structure de la table `accueil_note`
--

CREATE TABLE `accueil_note` (
  `id` bigint(20) NOT NULL,
  `note` double NOT NULL,
  `etudiant_id` bigint(20) NOT NULL,
  `evaluation_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `accueil_note`
--

INSERT INTO `accueil_note` (`id`, `note`, `etudiant_id`, `evaluation_id`) VALUES
(1, 10, 4, 1),
(2, 13, 6, 1),
(3, 15, 5, 3),
(4, 12, 4, 2),
(5, 13, 6, 2),
(6, 13, 10, 2),
(7, 12, 11, 1),
(8, 10, 11, 2);

-- --------------------------------------------------------

--
-- Structure de la table `accueil_paiement`
--

CREATE TABLE `accueil_paiement` (
  `id` bigint(20) NOT NULL,
  `montant_verse` decimal(10,2) NOT NULL,
  `date_paiement` date NOT NULL,
  `frais_total` decimal(10,2) NOT NULL,
  `deja_paye` decimal(10,2) NOT NULL,
  `reste_a_payer` decimal(10,2) NOT NULL,
  `numero_recu` varchar(50) NOT NULL,
  `etudiant_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `accueil_paiement`
--

INSERT INTO `accueil_paiement` (`id`, `montant_verse`, `date_paiement`, `frais_total`, `deja_paye`, `reste_a_payer`, `numero_recu`, `etudiant_id`) VALUES
(2, 200000.00, '2026-04-08', 350000.00, 0.00, 150000.00, 'RECU-2026-001', 5),
(3, 200000.00, '2026-04-29', 400000.00, 0.00, 200000.00, 'RECU-2026-002', 11);

-- --------------------------------------------------------

--
-- Structure de la table `accueil_presence`
--

CREATE TABLE `accueil_presence` (
  `id` bigint(20) NOT NULL,
  `statut` varchar(10) NOT NULL,
  `date` date NOT NULL,
  `emploi_id` bigint(20) NOT NULL,
  `etudiant_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `accueil_presence`
--

INSERT INTO `accueil_presence` (`id`, `statut`, `date`, `emploi_id`, `etudiant_id`) VALUES
(1, 'present', '2026-04-27', 3, 4),
(2, 'present', '2026-04-27', 3, 6),
(3, 'present', '2026-04-27', 3, 10),
(4, 'absent', '2026-04-27', 3, 11),
(5, 'present', '2026-04-27', 3, 4),
(6, 'present', '2026-04-27', 3, 6),
(7, 'present', '2026-04-27', 3, 10),
(8, 'present', '2026-04-27', 3, 11),
(9, 'present', '2026-04-27', 3, 4),
(10, 'present', '2026-04-27', 3, 6),
(11, 'present', '2026-04-27', 3, 10),
(12, 'present', '2026-04-27', 3, 11),
(13, 'absent', '2026-04-27', 3, 4),
(14, 'present', '2026-04-27', 3, 6),
(15, 'present', '2026-04-27', 3, 10),
(16, 'present', '2026-04-27', 3, 11),
(17, 'present', '2026-04-28', 4, 7),
(18, 'present', '2026-04-28', 5, 7);

-- --------------------------------------------------------

--
-- Structure de la table `accueil_student`
--

CREATE TABLE `accueil_student` (
  `id` bigint(20) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `date_naissance` date NOT NULL,
  `sexe` varchar(1) NOT NULL,
  `adresse` varchar(200) NOT NULL,
  `telephone` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(255) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `role` varchar(100) NOT NULL,
  `nom_parent` varchar(100) NOT NULL,
  `telephone_parent` varchar(20) NOT NULL,
  `date_inscription` datetime(6) NOT NULL,
  `filiere_id` bigint(20) DEFAULT NULL,
  `formation` varchar(255) NOT NULL DEFAULT 'DQP'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `accueil_student`
--

INSERT INTO `accueil_student` (`id`, `nom`, `prenom`, `date_naissance`, `sexe`, `adresse`, `telephone`, `email`, `password`, `photo`, `role`, `nom_parent`, `telephone_parent`, `date_inscription`, `filiere_id`, `formation`) VALUES
(4, 'Ebong nguedeu', 'Astride felixe', '2007-07-26', 'F', 'PK12', '656680215', 'astridnguedeu@gmail.com', 'a87b3e348ccb598ecb71bb83300a2bf8d91b780d0717aec6c91fb46ce6fbe3d8', '', 'student', 'mama', '667788909', '2026-04-08 16:17:13.553618', 6, 'CQP'),
(5, 'ATCHETNGNIA TCHATCHOUA', 'Darelle', '2006-04-10', 'F', 'KOTTO', '673773941', 'tchatchouadarelle@gmail.com', 'fdcbd22964851e47f38d17d2485d573c90ea26fb119dca69fa4d04bf593b646f', '', 'student', 'TCHATCHOUA BERLIN', '677208547', '2026-04-08 16:21:36.868105', 3, 'CQP'),
(6, 'peyebouo ', 'manuela doriane', '2003-03-11', 'F', 'DEIDO', '671544111', 'peyebouomanuela123@gmail.com', 'a2b2729d5e8f2d69ef437c3f250a516ca28e699dd1a10d30d143a3691d5b0943', '', 'student', 'hjjk', '678900432', '2026-04-08 16:30:55.141542', 6, 'DQP'),
(7, 'brayan ', 'noula', '2026-04-03', 'M', 'douala', '6772626365', 'brayan@gmail.com', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', '', 'student', 'noula', '6546377267', '2026-04-08 16:35:16.095290', 4, 'DQP'),
(9, 'nzali ', 'bryan', '2007-01-05', 'M', 'Douala PK 14', '655473150', 'nzalibryan@gmail.com', '352679c3ffea642a98db5219ca62b18037776a5f1e0ba946b352702c24e5b104', '', 'student', 'Mefang Domché', '695914186', '2026-04-08 16:44:39.833671', 11, 'DQP'),
(10, 'KEUBOU ', 'DINEL', '2026-04-21', 'M', 'DEIDO', '677345678', 'keubou@123.com', '8c7ab4e8f57b4da9da0a00a6fd82c9f836c9365b9029b70703e3b700ebd56fef', '', 'student', 'KEU ', '673456789', '2026-04-20 15:59:02.025554', 6, 'DQP'),
(11, 'KENFACK', 'FATIN', '2026-03-30', 'M', 'DEIDO', '677204567', 'fatin@gmail.com', 'a4a73786d46c671eceb6fe3ee28851df3b765a2fdc247a82f6795d2e1975c943', '', 'student', 'KENFACK PIERRE', '677204560', '2026-04-27 15:16:49.866966', 6, 'DQP');

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 3, 'add_permission'),
(6, 'Can change permission', 3, 'change_permission'),
(7, 'Can delete permission', 3, 'delete_permission'),
(8, 'Can view permission', 3, 'view_permission'),
(9, 'Can add group', 2, 'add_group'),
(10, 'Can change group', 2, 'change_group'),
(11, 'Can delete group', 2, 'delete_group'),
(12, 'Can view group', 2, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add admin', 7, 'add_admin'),
(26, 'Can change admin', 7, 'change_admin'),
(27, 'Can delete admin', 7, 'delete_admin'),
(28, 'Can view admin', 7, 'view_admin'),
(29, 'Can add enseignant', 10, 'add_enseignant'),
(30, 'Can change enseignant', 10, 'change_enseignant'),
(31, 'Can delete enseignant', 10, 'delete_enseignant'),
(32, 'Can view enseignant', 10, 'view_enseignant'),
(33, 'Can add filiere', 11, 'add_filiere'),
(34, 'Can change filiere', 11, 'change_filiere'),
(35, 'Can delete filiere', 11, 'delete_filiere'),
(36, 'Can view filiere', 11, 'view_filiere'),
(37, 'Can add cours', 8, 'add_cours'),
(38, 'Can change cours', 8, 'change_cours'),
(39, 'Can delete cours', 8, 'delete_cours'),
(40, 'Can view cours', 8, 'view_cours'),
(41, 'Can add emploi du temps', 9, 'add_emploidutemps'),
(42, 'Can change emploi du temps', 9, 'change_emploidutemps'),
(43, 'Can delete emploi du temps', 9, 'delete_emploidutemps'),
(44, 'Can view emploi du temps', 9, 'view_emploidutemps'),
(45, 'Can add student', 13, 'add_student'),
(46, 'Can change student', 13, 'change_student'),
(47, 'Can delete student', 13, 'delete_student'),
(48, 'Can view student', 13, 'view_student'),
(49, 'Can add paiement', 12, 'add_paiement'),
(50, 'Can change paiement', 12, 'change_paiement'),
(51, 'Can delete paiement', 12, 'delete_paiement'),
(52, 'Can view paiement', 12, 'view_paiement'),
(53, 'Can add note', 15, 'add_note'),
(54, 'Can change note', 15, 'change_note'),
(55, 'Can delete note', 15, 'delete_note'),
(56, 'Can view note', 15, 'view_note'),
(57, 'Can add evaluation', 14, 'add_evaluation'),
(58, 'Can change evaluation', 14, 'change_evaluation'),
(59, 'Can delete evaluation', 14, 'delete_evaluation'),
(60, 'Can view evaluation', 14, 'view_evaluation'),
(61, 'Can add presence', 16, 'add_presence'),
(62, 'Can change presence', 16, 'change_presence'),
(63, 'Can delete presence', 16, 'delete_presence'),
(64, 'Can view presence', 16, 'view_presence');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(7, 'accueil', 'admin'),
(8, 'accueil', 'cours'),
(9, 'accueil', 'emploidutemps'),
(10, 'accueil', 'enseignant'),
(14, 'accueil', 'evaluation'),
(11, 'accueil', 'filiere'),
(15, 'accueil', 'note'),
(12, 'accueil', 'paiement'),
(16, 'accueil', 'presence'),
(13, 'accueil', 'student'),
(1, 'admin', 'logentry'),
(2, 'auth', 'group'),
(3, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'accueil', '0001_initial', '2026-04-08 11:42:01.815910'),
(2, 'contenttypes', '0001_initial', '2026-04-08 11:42:01.876509'),
(3, 'auth', '0001_initial', '2026-04-08 11:42:02.475798'),
(4, 'admin', '0001_initial', '2026-04-08 11:42:02.604230'),
(5, 'admin', '0002_logentry_remove_auto_add', '2026-04-08 11:42:02.618379'),
(6, 'admin', '0003_logentry_add_action_flag_choices', '2026-04-08 11:42:02.632284'),
(7, 'contenttypes', '0002_remove_content_type_name', '2026-04-08 11:42:02.741105'),
(8, 'auth', '0002_alter_permission_name_max_length', '2026-04-08 11:42:02.808919'),
(9, 'auth', '0003_alter_user_email_max_length', '2026-04-08 11:42:02.856471'),
(10, 'auth', '0004_alter_user_username_opts', '2026-04-08 11:42:02.870698'),
(11, 'auth', '0005_alter_user_last_login_null', '2026-04-08 11:42:02.947547'),
(12, 'auth', '0006_require_contenttypes_0002', '2026-04-08 11:42:02.952271'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2026-04-08 11:42:02.982556'),
(14, 'auth', '0008_alter_user_username_max_length', '2026-04-08 11:42:03.041780'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2026-04-08 11:42:03.086881'),
(16, 'auth', '0010_alter_group_name_max_length', '2026-04-08 11:42:03.132098'),
(17, 'auth', '0011_update_proxy_permissions', '2026-04-08 11:42:03.161228'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2026-04-08 11:42:03.213561'),
(19, 'sessions', '0001_initial', '2026-04-08 11:42:03.278804'),
(20, 'accueil', '0002_student_formation', '2026-04-08 13:55:00.717248'),
(21, 'accueil', '0003_evaluation_note', '2026-04-10 11:38:09.204621'),
(22, 'accueil', '0004_evaluation_sequence', '2026-04-13 13:17:36.840483'),
(23, 'accueil', '0005_presence', '2026-04-27 16:28:09.894053');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('5h0k2ivtiafyja44a06r6mbobrebxrbk', '.eJyrVkrNK07NTM9LzCuJz0xRsjLRQRbJy89VslJycox0VUIRL8rPSVWyUipJTUzOSC1SqgUAhgwY7g:1wHi1E:jRAV8JXzt1DS5mh2CKB-7cMf5BTNACIgTCoDDcXEojA', '2026-05-12 12:58:28.294458'),
('ddswuy8bevnwkza8mgzcbig7b1hs4ic6', '.eJyrVkpMyc3Mi89MUbIy1IFyivJzUpWsIBylWgDWYQvu:1wHhsy:-xZ4O0urCnK3sntnQJjwyfGEUcscKazwtr8hHV2YxYM', '2026-05-12 12:49:56.266609'),
('dsjagqsu9t7objtsiqg67z661uk11jxm', '.eJyrVkotKU3JTMwric9MUbIyNNRBCOTl5ypZKXm7-rk5OnsruDmGePopIUkX5eekKlkpFZeUpqTmlSjVAgC7WRlB:1wI6gh:yPdqz-lM66_IO70ece7tJfowebM2z_iWFfDoAG2ctPk', '2026-05-13 15:18:55.443098'),
('ejfs86b9tutt65ny0c9z2sezh7yhq6w5', '.eJyrVkrNK07NTM9LzCuJz0xRsjLRQRbJy89VslJycox0VUIRL8rPSVWyUipJTUzOSC1SqgUAhgwY7g:1wCGIW:FlbvJglsFDMPfPdTF67NLAekwp4vLiK2Z6EqcJwSCpo', '2026-04-27 12:21:48.416062'),
('kqpa86le1z0u2yboiesxa2d2vmh2olwg', '.eJyrVkotKU3JTMwric9MUbIyNNRBCOTl5ypZKXm7-rk5OnsruDmGePopIUkX5eekKlkpFZeUpqTmlSjVAgC7WRlB:1wHhB2:7i_KMmsR0_NMbHgLeWaUGI61YteEa94vt6O7kLDZvc0', '2026-05-12 12:04:32.766073'),
('oazqtoag9g2fcmzik0gao4tmo4kaaj6u', '.eJyrVkpMyc3Mi89MUbIy1IFyivJzUpWsIBylWgDWYQvu:1wARPN:_lTA6SvcYDzzuah6KhpTc4PuZGvjfhjDoUeIS8bYRnY', '2026-04-22 11:49:21.692070'),
('ptiq6o8hc2g1gstlpo11kf5sq1wnt0e4', '.eJyrVkrNK07NTM9LzCuJz0xRsjLRQRbJy89VslJycox0VUIRL8rPSVWyUipJTUzOSC1SqgUAhgwY7g:1wHhyg:t8KrfnPkXUfUeVf-sVYZs7qjheZ3XPABYFivRWXaQ2Q', '2026-05-12 12:55:50.666641'),
('v29h6h5qkswgq1h9e2xpoh8ts1dqnnl4', '.eJyrVkrNK07NTM9LzCuJz0xRsjLRQRbJy89VslJycox0VUIRL8rPSVWyUipJTUzOSC0CyZWUpmTCzDA0RBKAGOHt6ufm6Oyt4OYY4umHrB5qUnFJaUpqXolSLQA6mjFi:1wHi0f:PxClAtW2sI5skuUGkgp2L_jH6ZkMELdO3HjY6nwPYNc', '2026-05-12 12:57:53.960326'),
('wkfryuyrfftjhqyncadf1ufm6fd77a4o', '.eJyrVkrNK07NTM9LzCuJz0xRsjLRQRbJy89VslJycox0VUIRL8rPSVWyUipJTUzOSC1SqgUAhgwY7g:1wHkQb:ZPVc4cFnstvzD6vQ9hNZMNuac5SS7m2jnrpIqIm9XZI', '2026-05-12 15:32:49.909050');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `accueil_admin`
--
ALTER TABLE `accueil_admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Index pour la table `accueil_cours`
--
ALTER TABLE `accueil_cours`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `accueil_cours_enseignant_id_98f015cf_fk_accueil_enseignant_id` (`enseignant_id`),
  ADD KEY `accueil_cours_filiere_id_7804c6e6_fk_accueil_filiere_id` (`filiere_id`);

--
-- Index pour la table `accueil_emploidutemps`
--
ALTER TABLE `accueil_emploidutemps`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accueil_emploidutemp_enseignant_id_c651bc27_fk_accueil_e` (`enseignant_id`),
  ADD KEY `accueil_emploidutemps_cours_id_95982259_fk_accueil_cours_id` (`cours_id`),
  ADD KEY `accueil_emploidutemps_filiere_id_62643b94_fk_accueil_filiere_id` (`filiere_id`);

--
-- Index pour la table `accueil_enseignant`
--
ALTER TABLE `accueil_enseignant`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Index pour la table `accueil_evaluation`
--
ALTER TABLE `accueil_evaluation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accueil_evaluation_cours_id_ae185a1c_fk_accueil_cours_id` (`cours_id`),
  ADD KEY `accueil_evaluation_filiere_id_00bb00b2_fk_accueil_filiere_id` (`filiere_id`);

--
-- Index pour la table `accueil_filiere`
--
ALTER TABLE `accueil_filiere`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `accueil_note`
--
ALTER TABLE `accueil_note`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accueil_note_etudiant_id_debb4ec2_fk_accueil_student_id` (`etudiant_id`),
  ADD KEY `accueil_note_evaluation_id_1944acf1_fk_accueil_evaluation_id` (`evaluation_id`);

--
-- Index pour la table `accueil_paiement`
--
ALTER TABLE `accueil_paiement`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_recu` (`numero_recu`),
  ADD KEY `accueil_paiement_etudiant_id_7481ab08_fk_accueil_student_id` (`etudiant_id`);

--
-- Index pour la table `accueil_presence`
--
ALTER TABLE `accueil_presence`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accueil_presence_emploi_id_38cf6f3b_fk_accueil_emploidutemps_id` (`emploi_id`),
  ADD KEY `accueil_presence_etudiant_id_f1ed477a_fk_accueil_student_id` (`etudiant_id`);

--
-- Index pour la table `accueil_student`
--
ALTER TABLE `accueil_student`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `accueil_student_filiere_id_ab8852a3_fk_accueil_filiere_id` (`filiere_id`);

--
-- Index pour la table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Index pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Index pour la table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Index pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Index pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Index pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Index pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `accueil_admin`
--
ALTER TABLE `accueil_admin`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `accueil_cours`
--
ALTER TABLE `accueil_cours`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT pour la table `accueil_emploidutemps`
--
ALTER TABLE `accueil_emploidutemps`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `accueil_enseignant`
--
ALTER TABLE `accueil_enseignant`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `accueil_evaluation`
--
ALTER TABLE `accueil_evaluation`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `accueil_filiere`
--
ALTER TABLE `accueil_filiere`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT pour la table `accueil_note`
--
ALTER TABLE `accueil_note`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `accueil_paiement`
--
ALTER TABLE `accueil_paiement`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `accueil_presence`
--
ALTER TABLE `accueil_presence`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT pour la table `accueil_student`
--
ALTER TABLE `accueil_student`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT pour la table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT pour la table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `accueil_cours`
--
ALTER TABLE `accueil_cours`
  ADD CONSTRAINT `accueil_cours_enseignant_id_98f015cf_fk_accueil_enseignant_id` FOREIGN KEY (`enseignant_id`) REFERENCES `accueil_enseignant` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `accueil_cours_filiere_id_7804c6e6_fk_accueil_filiere_id` FOREIGN KEY (`filiere_id`) REFERENCES `accueil_filiere` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `accueil_emploidutemps`
--
ALTER TABLE `accueil_emploidutemps`
  ADD CONSTRAINT `accueil_emploidutemp_enseignant_id_c651bc27_fk_accueil_e` FOREIGN KEY (`enseignant_id`) REFERENCES `accueil_enseignant` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `accueil_emploidutemps_cours_id_95982259_fk_accueil_cours_id` FOREIGN KEY (`cours_id`) REFERENCES `accueil_cours` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `accueil_emploidutemps_filiere_id_62643b94_fk_accueil_filiere_id` FOREIGN KEY (`filiere_id`) REFERENCES `accueil_filiere` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `accueil_evaluation`
--
ALTER TABLE `accueil_evaluation`
  ADD CONSTRAINT `accueil_evaluation_cours_id_ae185a1c_fk_accueil_cours_id` FOREIGN KEY (`cours_id`) REFERENCES `accueil_cours` (`id`),
  ADD CONSTRAINT `accueil_evaluation_filiere_id_00bb00b2_fk_accueil_filiere_id` FOREIGN KEY (`filiere_id`) REFERENCES `accueil_filiere` (`id`);

--
-- Contraintes pour la table `accueil_note`
--
ALTER TABLE `accueil_note`
  ADD CONSTRAINT `accueil_note_etudiant_id_debb4ec2_fk_accueil_student_id` FOREIGN KEY (`etudiant_id`) REFERENCES `accueil_student` (`id`),
  ADD CONSTRAINT `accueil_note_evaluation_id_1944acf1_fk_accueil_evaluation_id` FOREIGN KEY (`evaluation_id`) REFERENCES `accueil_evaluation` (`id`);

--
-- Contraintes pour la table `accueil_paiement`
--
ALTER TABLE `accueil_paiement`
  ADD CONSTRAINT `accueil_paiement_etudiant_id_7481ab08_fk_accueil_student_id` FOREIGN KEY (`etudiant_id`) REFERENCES `accueil_student` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `accueil_presence`
--
ALTER TABLE `accueil_presence`
  ADD CONSTRAINT `accueil_presence_emploi_id_38cf6f3b_fk_accueil_emploidutemps_id` FOREIGN KEY (`emploi_id`) REFERENCES `accueil_emploidutemps` (`id`),
  ADD CONSTRAINT `accueil_presence_etudiant_id_f1ed477a_fk_accueil_student_id` FOREIGN KEY (`etudiant_id`) REFERENCES `accueil_student` (`id`);

--
-- Contraintes pour la table `accueil_student`
--
ALTER TABLE `accueil_student`
  ADD CONSTRAINT `accueil_student_filiere_id_ab8852a3_fk_accueil_filiere_id` FOREIGN KEY (`filiere_id`) REFERENCES `accueil_filiere` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Contraintes pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Contraintes pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
